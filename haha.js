/**
 * Created by admin on 2018/6/25.
 */


// console.log(true && true);
// console.log(false || true);
// console.log(!false)

// function yes() {
//     console.log('yes')
//     return true
// }
// function no() {
//     console.log('no')
//     return false
// }
// console.log(yes() || no())
// console.log(yes() && no())


let arr = [1,2,3,4,5]
let obj = {
    a:1,
    b:2,
    c:3
}

for (let idx in arr){
    console.log(idx)
}
for (let idx in obj) {
    console.log(`${idx} => ${obj[idx]}`)
}
let x
for (let i=1;i<10;i++) {
    console.log(i)
}