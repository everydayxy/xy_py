import config, util

import normalservice

def run(game_id, server_id, log_name, req, args):
    '''
    /rest/user_acitve_info
    args:
        on: 'active_day', 'seq_active_day', 'user_count', 'user_count_rank',
            'newuser_lost_ratio_week', 'newuser_lost_ratio_biweek','newuser_lost_ratio_month', 'newuser_count',
            'user_lost_ratio_week', 'user_lost_ratio_rank', 'user_lost_ratio_biweek', 'user_lost_ratio_month', 'user_back_ratio_week', 'user_back_ratio_biweek',
            'online_time', 'online_count', 'average_online_time', 'rank_online_time', 'login_count', 'exit_count',
            'consumer_summary', 'consumer_behavior_lost_ratio_week', 'consumer_behavior_lost_ratio_biweek', 'consumer_behavior_lost_ratio_month',
            'consumer_behavior_count', 'consumer_behavior_rank'
        groupby: 'allusers':0, 'newusers', 'activeusers', 'new_activeusers', 'consumers', 'non-consumers'
    '''
    desc_path = config.LOG_DIR + '/' + game_id + '/desc/'
    path = config.LOG_DIR + '/' + game_id + '/' + server_id
    on_field = args.get('on')
    groupby = args.get('groupby')
    start_date = args.get('start_time')
    end_date = args.get('end_time')
    if on_field in normalservice.services and start_date != None:
        ns = normalservice.NormalStatisticService()
        ret_data = ns.get_roles_info(desc_path, path, start_date, end_date, on_field, groupby)
        req.write(ret_data)
    req.finish()
