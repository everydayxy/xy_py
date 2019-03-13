<?php
/**
 * Created by PhpStorm.
 * User: Sweerinn
 * Date: 2017/12/8
 * Time: 14:53
 */

function getMemory() {
    return floor(memory_get_usage()/1024/1024);
}

class Base {
    protected function notify( $msg, $cl = 32 ) {
        $format = "\033[%dm%s\033[0m\n";
        echo sprintf( $format, $cl, $msg );
    }

    protected function snotify( $msg, $cl = 32 ) {
        $format = "\033[%dm%s\033[0m";
        echo sprintf( $format, $cl, $msg );
    }
    
    protected function execute($sql,$conn = ''){
        $res = @pg_query($conn,$sql);
        if(!$res){
            $msg = sprintf("执行Sql失败: %s,错误信息: %s",$sql, pg_last_error($conn));
            throw new Exception($msg);
        }
        return $res;
    }
    
    protected function get_max_id( $table, $field ) {
        $sql = "SELECT max($field) FROM $table";
        $res = $this->execute($sql,$this->master_conn);
        $row = pg_fetch_row( $res );
        if ( $row[0] ) {
            return $row[0];
        } else {
            return 0;
        }
    }
}

class ExistsName extends Base {
    protected $crops_name = array();
    protected $role_name = array();
    protected $repeat_role_id = array();
    protected $repeat_crop_id = array();
    
    public function __construct() {
    }
    
    public function get_repeat_role_name() {
        return $this->repeat_role_id;
    }
    
    public function get_repeat_crop_name() {
        return $this->repeat_crop_id;
    }
    
    public function checkCropName( $name, $id = 0 ) {
        if ( array_key_exists( $name, $this->crops_name ) ) {
            $this->crops_name[ $name ] ++;
            array_push( $this->repeat_crop_id, $id );
            
            return $name . '__' . $this->crops_name[ $name ];
        } else {
            $this->crops_name[ $name ] = 0;
            
            return $name;
        }
    }
    
    public function checkRoleName( $name, $id ) {
        if ( array_key_exists( $name, $this->role_name ) ) {
            $this->role_name[ $name ] ++;
            array_push( $this->repeat_role_id, $id );
            
            return $name . '__' . $this->role_name[ $name ];
        } else {
            $this->role_name[ $name ] = 0;
            
            return $name;
        }
        
    }
}

class NewPlayerId extends Base {
    protected $roles = array();
    
    public function __construct() {
    }
    
    public function addId( $old_id, $new_id ) {
        $this->roles[ $old_id ] = $new_id;
    }
    
    public function getId( $old_id ) {
        if ( array_key_exists( $old_id, $this->roles ) ) {
            return $this->roles[ $old_id ];
        } else {
            $msg = '角色ID:' . $old_id . ",不存在";
            $e = new Exception( $msg );
            echo $e->getMessage() . "\n";
            throw $e;
        }
    }
}

class ImportDb extends Base {
    public function __construct( $filename ) {
        $this->filename = $filename;
        $this->pathinfo = pathinfo( $this->filename );
        $conn = pg_connect( 'host=db dbname=postgres user=postgres port=5432' );
        if ( empty( $conn ) ) {
            die( "连接数据库失败\n" );
        }
        $this->conn = $conn;
        if ( ! $this->check_db_file_exists() ) {
            die( "数据库备份文件不存在\n" );
        }
    }
    
    private function check_db_file_exists() {
        if ( file_exists( $this->filename ) ) {
            return true;
        } else {
            return false;
        }
    }
    
    public function get_db_name() {
        return str_replace( '-', '_', $this->pathinfo['filename'] );
    }
    
    public static function import( $filename ) {
        $model = new static( $filename );
        $db = $model->get_db_name();
        $sql = "drop database if exists $db";
        $model->execute($sql,$model->conn);
        $model->execute("create database $db",$model->conn);
        system( "sudo psql -h db -U postgres " . $db . " -f " . $model->filename );
        
        return pg_connect( "host=db dbname=$db user=postgres" );
    }
}


class Comb extends Base {
    protected $conn = null;
    private $accidModel = null;
    private $deleteAcc = array();
    private $slave_conn = null;
    public $master_conn = null;
    private $is_first = null;
    private $exists_player = null;
    public $start_time = 0;
    public $end_time = 0;
    public $max_id = 0;
    
    public function __construct( $master_conn, $slave_conn, $exists_player, $is_first = false ) {
        $this->start_time = time();
        $this->accidModel = new NewPlayerId();
        $this->master_conn = $master_conn;
        $this->slave_conn = $slave_conn;
        $this->exists_player = $exists_player;
        $this->is_first = $is_first;
        $this->max_id = $this->get_max_id( 'roles', 'id' );
        $msg = sprintf( "正在合并数据库: %s", pg_dbname( $this->slave_conn ) );
        $this->notify( $msg );
    }
    
    public function end_main() {
        // $sql = "drop database"
        $this->end_time = time();
        $msg = "数据库: %s,合并完成,单个数据库合并用时间%d秒";
        $this->notify( sprintf( $msg, pg_dbname( $this->slave_conn ), $this->end_time - $this->start_time ) );
        pg_close( $this->slave_conn );
    }
    
    private function filter_value( $arr ) {
        foreach ( $arr as $k => $v ) {
            $v = preg_replace( '/\n+/', '\n', $v );
            $v = preg_replace( '/\t+/', '\t', $v );
            $v = preg_replace( '/\r+/', '\r', $v );
            $arr[ $k ] = addslashes( $v );
        }
        
        return $arr;
    }
    
    private function import_data( $data, $table ) {
        if ( empty( $data ) ) {
            $msg = "当前数据库: %s, 表: %s,并没有数据,跳过";
            $this->notify( sprintf( $msg, pg_dbname( $this->slave_conn ), $table ), 31 );
            
            return;
        }
        $msg = "正在合并数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), $table ) );
        $tmepfile = tempnam( "./tmp/", $table );
        $fp = fopen( $tmepfile, "w" );
        $sql = sprintf( "COPY %s (%s) FROM '%s';\n", $table, join( ",", array_keys( $data[0] ) ), $tmepfile );
        $str = '';
        fwrite( $fp, $str );
        foreach ( $data as $row ) {
            $row = $this->filter_value( $row );
            $str = join( "\t", $row ) . "\n";
            fwrite( $fp, $str );
        }
        $str = '\.' . "\n";
        fwrite( $fp, $str );
        fclose( $fp );
        chmod($tmepfile,0604);
        $r = $this->execute($sql,$this->master_conn);
        if($r){
            unlink($tmepfile);
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
    }

    private function get_single_table() {
        return array(
            'activity_records'         => 'role_id',
            'activity_shop_records'    => 'role_id',
            'all_power_lv'    => 'role_id',
            'annis'    => 'role_id',
            'bind_phone'   => 'role_id',
            'cd_times'         => 'role_id',
//            'champion_race_ranks'         => 'role_id', //是否处理待定
            'chest_helps'         => 'role_id', //players包含sid和loginname
            'crop_boss_draw_flags'         => 'role_id',
            'crop_boss_times'         => 'role_id',
            'guides'         => 'role_id',
            'herocollect'         => 'role_id',
            'instance_activities'         => 'role_id',
            'instance_star_drawns'         => 'role_id',
            'intimacys'         => 'role_id',
            'legends'         => 'role_id',
            'level_acts'         => 'role_id',
            'limited_hero_states'         => 'role_id',
            'materials'         => 'role_id',
            'pets'         => 'role_id',
            'recruits'         => 'role_id',
            'role_ex'         => 'role_id',
            'role_pays'         => 'role_id',
            'signs'         => 'role_id',
            'standards'         => 'role_id',
            'startech'         => 'role_id',
            'supply'         => 'role_id',
            'tactics'         => 'role_id',
            'tasks'         => 'role_id',
            'timer_fields'         => 'role_id',
            'towers'         => 'role_id',
            'titles'         => 'role_id',
            'wheels'         => 'role_id',
        );
    }
    
    private function get_mutl_table() {
        return array(
            'formations'            => 'role_id',
            'heros'            => 'role_id',
            'instances'            => 'role_id',
            'items'            => 'role_id',
            'shops'            => 'role_id',
        );
    }

    private function get_table_with_increaseid() {
        return array(
            'chests'            => 'role_id',
            'honor_logs'            => 'role_id',
            'redbags'            => 'role_id',
            'pay_order'            => 'role_id',
        );
    }
    //activity_shops
    //activity_stats
    //arena_logs
    //arena_rank
    //broad_msgs
    //common_activitys

    //crop_war_battle_logs
    //crop_war_crop_beat_logs
    //crop_war_crop_ranks
    //crop_war_member_ranks
    //fight_logs 是否清空
    //gift_cards
    //global_batch_mails
    //global_mails
    //rank_activitys
    //reward_activitys
    //server_params
    //special_activity_records
    //special_activitys
    
    //crop_apply_members, crop_be_apply_members, crop_logs, crop_members, crops
    
    private function process_server_params() {
        if ( $this->is_first ) {
            $sql = "SELECT * FROM crop_boss";
            $res = $this->execute($sql,$this->slave_conn);
            $data = array();
            while ( $row = pg_fetch_assoc( $res ) ) {
                array_push( $data, $row );
            }
            $this->import_data( $data, 'crop_boss' );

            $sql = "SELECT * FROM server_params";
            $res = $this->execute($sql,$this->slave_conn);
            $data = array();
            while ( $row = pg_fetch_assoc( $res ) ) {
                array_push( $data, $row );
            }
            $this->import_data( $data, 'server_params' );
        }
    }
    
    private function process_mail() {
        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'mails' ) );
        $sql = "DELETE FROM mails WHERE state = 2 or (state = 1 and rewards='')";
        $this->execute($sql,$this->slave_conn);
        $sql = sprintf("DELETE FROM mails WHERE ts < %s", time() - 24 * 3600 * 15);
        $this->execute($sql,$this->slave_conn);
        $sql = "SELECT * FROM mails";
        $data = array();
        $max_id = $this->get_max_id( 'mails', 'id' );
        $res = $this->execute($sql,$this->slave_conn);
        while ( $row = pg_fetch_assoc( $res ) ) {
            try {
                $row[ 'role_id' ] = $this->accidModel->getId( $row[ 'role_id' ] );
            } catch ( Exception $e ) {
                continue;
            }
            $row['id'] = ++ $max_id;
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'mails' );

        $sql = sprintf("alter sequence mails_id_seq restart with %d", $max_id+1);
        $this->execute($sql,$this->master_conn);
    }
    
    private function check_crop_owner( $crop_id ) {
        $sql = "SELECT * FROM crop_members WHERE position=1 AND crop_id=" . $crop_id . " LIMIT 1";
        $res = $this->execute($sql,$this->slave_conn);
        $row = pg_fetch_assoc( $res );
        if ( empty( $row ) ) {
            return false;
        } else {
            return true;
        }
    }
    
    private function process_crops() {
        $max_id = $this->get_max_id( 'crops', 'id' );

        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'crops' ) );
        $sql = "SELECT * FROM crops";
        $res = $this->execute($sql,$this->slave_conn);
        $data = array();
        $crops_id = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            if ( ! $this->check_crop_owner( $row['id'] ) ) {
                $sql = "DELETE FROM crop_members WHERE crop_id=" . $row['id'];
                pg_query( $this->slave_conn, $sql );
                continue;
            }
            $crop_id = ++ $max_id;
            $crops_id[ $row['id'] ] = $crop_id;
            $row['id'] = $crop_id;
            $row['name'] = $this->exists_player->checkCropName( $row['name'], $crop_id );
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'crops' );

        $sql = sprintf("alter sequence crops_id_seq restart with %d", $max_id+1);
        $this->execute($sql,$this->master_conn);

        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'crop_members' ) );
        $sql = "SELECT * FROM crop_members";
        $res = $this->execute($sql,$this->slave_conn);
        $data = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            try {
                $accid = $this->accidModel->getId( $row[ 'role_id' ] );
            } catch ( Exception $e ) {
                continue;
            }
            if ( ! array_key_exists( $row['crop_id'], $crops_id ) ) {
                continue;
            }
            $row['crop_id'] = $crops_id[ $row['crop_id'] ];
            $row['role_id'] = $accid;
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'crop_members' );

        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'crop_apply_members' ) );
        $sql = "SELECT * FROM crop_apply_members";
        $res = $this->execute($sql,$this->slave_conn);
        $data = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            try {
                $accid = $this->accidModel->getId( $row[ 'role_id' ] );
            } catch ( Exception $e ) {
                continue;
            }
            if ( ! array_key_exists( $row['crop_id'], $crops_id ) ) {
                continue;
            }
            $row['crop_id'] = $crops_id[ $row['crop_id'] ];
            $row['role_id'] = $accid;
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'crop_apply_members' );

        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'crop_be_apply_members' ) );
        $sql = "SELECT * FROM crop_be_apply_members";
        $res = $this->execute($sql,$this->slave_conn);
        $data = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            try {
                $accid = $this->accidModel->getId( $row[ 'role_id' ] );
            } catch ( Exception $e ) {
                continue;
            }
            if ( ! array_key_exists( $row['crop_id'], $crops_id ) ) {
                continue;
            }
            $row['crop_id'] = $crops_id[ $row['crop_id'] ];
            $row['role_id'] = $accid;
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'crop_be_apply_members' );

        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'crop_logs' ) );
        $max_id = $this->get_max_id( 'crop_logs', 'id' );
        $sql = "SELECT * FROM crop_logs";
        $res = $this->execute($sql,$this->slave_conn);
        $data = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            if ( ! array_key_exists( $row['crop_id'], $crops_id ) ) {
                continue;
            }
            $row['id'] = ++ $max_id;
            $row['crop_id'] = $crops_id[ $row['crop_id'] ];
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'crop_logs' );

        $sql = sprintf("alter sequence crop_logs_id_seq restart with %d", $max_id+1);
        $this->execute($sql,$this->master_conn);

        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'crop_instances' ) );
        $sql = "SELECT * FROM crop_instances";
        $res = $this->execute($sql,$this->slave_conn);
        $data = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            if ( ! array_key_exists( $row['crop_id'], $crops_id ) ) {
                continue;
            }
            $row['crop_id'] = $crops_id[ $row['crop_id'] ];
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'crop_instances' );
    }
    
    private function process_roles() {
        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'roles' ) );
        $sql = "SELECT * FROM roles";
        $res = $this->execute($sql,$this->slave_conn);
        $roles = array();
        $accounts = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            $accid = ++ $this->max_id;
            $org_id = $row['id'];
            $row['id'] = $accid;
            $account_id = $row['account_id'];
            $acc = $this->process_accounts( $account_id, $accid );
            $row['account_id'] = $accid;
            $row['role_name'] = $this->exists_player->checkRoleName( $row['role_name'], $accid );
            $roles[] = $row;
            $accounts[] = $acc;
            $this->accidModel->addId( $org_id, $accid );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $roles, 'roles' );
        $this->import_data( $accounts, 'accounts' );
    }
    
    private function process_accounts( $id, $new_id ) {
        $sql = "SELECT * FROM accounts WHERE id=" . $id;
        $res = $this->execute($sql,$this->slave_conn);
        $row = pg_fetch_assoc( $res );
        $row['id'] = $new_id;
        
        return $row;
    }
    
    private function process_tables() {
        foreach ( $this->get_single_table() as $table => $pk ) {
            $msg = "正在处理数据库:%s,表:%s,请稍候......";
            $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), $table ) );
            $sql = "SELECT * FROM " . $table;
            $res = $this->execute($sql,$this->slave_conn);
            $data = array();
            while ( $row = pg_fetch_assoc( $res ) ) {
                try {
                    $row[ $pk ] = $this->accidModel->getId( $row[ $pk ] );
                } catch ( Exception $e ) {
                    continue;
                }
                
                array_push( $data, $row );
            }
            $this->notify(sprintf("ok! memory:%sM", getMemory()));
            $this->import_data( $data, $table );
        }

        foreach ( $this->get_mutl_table() as $table => $pk ) {
            $msg = "正在处理数据库:%s,表:%s,请稍候......";
            $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), $table ) );
            $sql = "SELECT * FROM " . $table;
            $res = $this->execute($sql,$this->slave_conn);
            $data = array();
            while ( $row = pg_fetch_assoc( $res ) ) {
                try {
                    $row[ $pk ] = $this->accidModel->getId( $row[ $pk ] );
                } catch ( Exception $e ) {
                    continue;
                }
                array_push( $data, $row );
            }
            $this->notify(sprintf("ok! memory:%sM", getMemory()));
            $this->import_data( $data, $table );
        }

        foreach ( $this->get_table_with_increaseid() as $table => $pk ) {
            $msg = "正在处理数据库:%s,表:%s,请稍候......";
            $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), $table ) );
            $max_id = $this->get_max_id( $table, 'id' );
            $sql = "SELECT * FROM " . $table;
            $res = $this->execute($sql,$this->slave_conn);
            $data = array();
            while ( $row = pg_fetch_assoc( $res ) ) {
                $row[ 'id' ] = ++ $max_id;
                try {
                    $row[ $pk ] = $this->accidModel->getId( $row[ $pk ] );
                } catch ( Exception $e ) {
                    continue;
                }
                array_push( $data, $row );
            }
            $this->notify(sprintf("ok! memory:%sM", getMemory()));
            $this->import_data( $data, $table );
            if ( $table == 'pay_order' ) {
                $sql = sprintf("alter sequence pay_order_id_seq restart with %d", $max_id+1);
                $this->execute($sql,$this->master_conn);
            }
            if ( $table == 'honor_logs' ) {
                $sql = sprintf("alter sequence honor_logs_id_seq restart with %d", $max_id+1);
                $this->execute($sql,$this->master_conn);
            }
        }
    }
    
    private function process_arena() {
        $msg = "正在处理数据库:%s,表:%s,请稍候......";
        $this->snotify( sprintf( $msg, pg_dbname( $this->slave_conn ), 'arenas' ) );
        $data = array();
        $sql = "SELECT * FROM arenas";
        $res = $this->execute($sql,$this->slave_conn);
        while ( $row = pg_fetch_assoc( $res ) ) {
            try {
                $row[ 'role_id' ] = $this->accidModel->getId( $row[ 'role_id' ] );
                $row[ 'reset_ts' ] = 0;
            } catch ( Exception $e ) {
                continue;
            }
            array_push( $data, $row );
        }
        $this->notify(sprintf("ok! memory:%sM", getMemory()));
        $this->import_data( $data, 'arenas' );
    }

    
    private function error( $msg ) {
        $format = "\033[33m当前数据库:%s,操作失败,失败原因:%s\033[0m\n";
        echo sprintf( $format, pg_dbname( $this->slave_conn ), $msg );
        die();
    }
    
    public function main() {
        $this->process_roles();
        $this->process_mail();
        $this->process_tables();
        $this->process_arena();
        $this->process_crops();
        $this->process_server_params();
        $this->end_main();
    }
}

class Main extends Base {
    private $options = array();
    public $master_conn = null;
    private $slave_conn = null;
    private $version = "1.0.0";
    private $start_time = 0;
    
    public function __construct() {
        $this->start_time = time();
        $this->parse_option();
        if ( array_key_exists( 'v', $this->options ) ) {
            $this->version = $this->options['v'];
        }
        
        $this->start();
    }
    
    
    
    private function parse_option() {
        // m 主数据库. s 要合并的数据库, 多个区服用逗号(,)分隔
        $this->options = getopt( "m:s:v:" );
    }
    
    public function start() {
        if ( empty( $this->options['m'] ) || empty( $this->options['s'] ) ) {
            die( "参数错误\n" );
        }
        $this->master_conn = $this->init_master();
        $file_list = explode( ",", $this->options['s'] );
        $exists_player = new ExistsName();
        $is_first = true;
        foreach ( $file_list as $filename ) {
            $filename = __DIR__ . '/' . $filename;
            if ( ! file_exists( $filename ) ) {
                continue;
            }
            $this->slave_conn = ImportDb::import( $filename );
            $comb = new Comb( $this->master_conn, $this->slave_conn, $exists_player, $is_first );
            $comb->main();
            $is_first = false;
        }
        $this->process_repeat_loginname();
//        $this->process_repeat_crops( $exists_player );
//        $this->set_rename_state( $exists_player );
        $this->export_master();
        die( sprintf( "合并数据库共用时间: %d 秒\n", time() - $this->start_time ) );
    }
    
    private function process_repeat_crops( $exists_player ) {
        $repeat_crop = $exists_player->get_repeat_crop_name();
        $max_id = $this->get_max_id( 'mails', 'id' );
        foreach ( $repeat_crop as $crop_id ) {
            $sql = "SELECT id FROM crop_members WHERE pos=1 AND crop_id=" . $crop_id . " LIMIT 1";
            $res = pg_query( $this->master_conn, $sql );
            $row = pg_fetch_assoc( $res );
            if ( empty( $row ) ) {
                $e =  new Exception( sprintf( "该军团没有军团长:%d\n", $crop_id ) );
                echo $e->getMessage();
                continue;
            }
            $role_id = $row['id'];
            $content = '由于您的区服已与其他区服合并，您的公会名在其他区服已被使用，故给予您补偿500钻石，您可打开“公会管理”按钮自助改名';
            $data = array(
                'id'          => ++ $max_id,
                'role_id'     => $role_id,
                'content'     => $content,
                'title'       => '合服公会改名津贴',
                'create_time' => time(),
                'type'        => 1,
                'is_read'     => 0,
                'is_drawn'    => 0,
                'rewards'     => '6,500,0'
            );
            pg_insert( $this->master_conn, 'mails', $data );
        }
    }
    
    private function process_repeat_loginname() {
        $this->notify( "查找重复的loginname" );
        $sql = "SELECT loginname,count(loginname) FROM accounts GROUP BY loginname HAVING count(loginname) > 1";
        $res = $this->execute($sql,$this->master_conn);
        $arr = array();
        while ( $row = pg_fetch_assoc( $res ) ) {
            if ( ! array_key_exists( $row['loginname'], $arr ) ) {
                $arr[ $row['loginname'] ] = array();
            }
            array_push( $arr, $row['loginname'] );
        }
        $removeAccounts = array();
        foreach ( $arr as $loginname ) {
            $sql = "select accounts.id as account_id, role_lvl from accounts,roles where accounts.id=roles.account_id and loginname='" . $loginname . "'";
            $res = $this->execute($sql,$this->master_conn);

            while ( $row = pg_fetch_assoc( $res ) ) {
                if ($row['role_lvl'] <= 1) {
                    array_push( $removeAccounts, $row['account_id']);
                }
            }
        }
        if (count($removeAccounts) > 0) {
            $this->snotify( "删除重复的且等级为1级的账号 ...... " );
            $sql = "delete from accounts where id in (" . join(',', $removeAccounts) . ")";
            $this->execute($sql,$this->master_conn);
            $this->notify( "ok" );
        } else {
            $this->snotify( "没有重复账号可被删除" );
        }
    }
    
    private function set_rename_state( $exists_player ) {
        $data = $exists_player->get_repeat_role_name();
        foreach ( $data as $id ) {
            $sql = "SELECT * FROM role_states WHERE id=" . $id;
            $res = $this->execute($sql,$this->master_conn);
            $row = pg_fetch_assoc( $res );
            if ( empty( $row ) ) {
                continue;
            }
            $state = explode( ",", $row['state_str'] );
            $state[1] = 0;
            $state = join( ",", $state );
            pg_update( $this->master_conn, 'role_states', array( 'state_str' => $state ), array( 'id' => $id ) );
        }
    }
    
    private function export_master() {
        $cmd = "pg_dump -h db -U postgres %s -f %s.sql";
        $db = pg_dbname( $this->master_conn );
        system( sprintf( $cmd, $db, $db ) );
    }
    
    private function init_master() {
        $schema = __DIR__ . "/v" . $this->version . "_schema.sql";
        if ( ! file_exists( $schema ) ) {
            die( "主数据库结构表不存在\n" );
        }
        $conn = pg_connect( "host=db dbname=postgres user=postgres" );
        if ( empty( $conn ) ) {
            die( "连接主数据库失败\n" );
        }
        $sql = "drop database if exists " . $this->options['m'];
        $this->execute($sql,$conn);
        $sql = "create database " . $this->options['m'];
        $this->execute($sql,$conn);
        if ( ! pg_last_error( $conn ) ) {
            system( "sudo psql -h db -U postgres " . $this->options['m'] . " -f " . $schema );
            return pg_connect( "host=db dbname=" . $this->options['m'] . " user=postgres" );
        } else {
            return false;
        }
    }
}

$model = new Main();


?>