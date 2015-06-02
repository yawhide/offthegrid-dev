// this is the script I used to get all the vendors from the offthegrid website.
// I stringified them, copied the output to my create_test_entries.txt which saved the info into the db
var $trucks = document.querySelectorAll('#food-tab .otg-vendor-type-0 table tr.otg-vendor')
var $carts = document.querySelectorAll('#food-tab .otg-vendor-type-1 tr.otg-vendor')
var $tents = document.querySelectorAll('#food-tab .otg-vendor-type-2 tr.otg-vendor')

function parse(arr, type){
  var data = []
  for (var i = arr.length - 1; i >= 0; i--) {
    var ob = {
      name: arr[i].querySelector('.otg-vendor-name-link').innerText,
      food: arr[i].querySelector('.otg-vendor-cuisines').innerText,
      img: arr[i].querySelector('.otg-vendor-logo').src,
      type: type,
      url: arr[i].querySelector('.otg-vendor-logo-link').href,
    }
    data.push(ob)
  };
  return data
}

console.log(JSON.stringify(parse($trucks, 'truck')))
console.log(JSON.stringify(parse($carts, 'cart')))
console.log(JSON.stringify(parse($tents, 'tent')))
