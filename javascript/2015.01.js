var fs = require("fs");
inp = fs
  .readFileSync(0) // STDIN_FILENO = 0
  .toString().trim();

let one = inp.split('').reduce((o, c) => o += (c=='(')*2 - 1, 0);
console.log(one);

let two = (inp => {
  let floor = 0;
  for (let i = 0, l = inp.length; i < l; i++) {
    let v = inp[i];
    floor += (v == '(') * 2 - 1;
    if (floor < 0) return i + 1
  }
})(inp);

console.log(two)
