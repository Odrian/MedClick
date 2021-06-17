window.addEventListener('load', (event) => update_corols());

function update_corols() {
  var tr = document.getElementById("tbody").getElementsByTagName('tr');
  var j = 0;
  for (var i = 0; i < tr.length; i++) {
    if (!tr[i].classList.contains("hidden")) {
      if (j % 2 == 1) {
        tr[i].style.background = "#f8f8f8";
      } else {
        tr[i].style.background = "#ffffff";
      }
      j++;
    }
  }
}

function search() {
  var phone, name;
  var filter = document.getElementById('searchbar').value.toLowerCase();
  var tr = document.getElementById("tbody").getElementsByTagName('tr');
  for (var i = 0; i < tr.length; i++) {
    phone = tr[i].getElementsByClassName("phone")[0].firstChild.textContent;
    name = tr[i].getElementsByClassName("name")[0].textContent.toLowerCase();
    if (phone.indexOf(filter) > -1 || name.indexOf(filter) > -1) {
      tr[i].classList.remove("hidden-search");
    } else {
      tr[i].classList.add("hidden-search");
    }
  }
  update_corols();
}

function filter(type, value) {
  var li = document.getElementById(type).getElementsByTagName("*");
  for (var i = 0; i < li.length; i++) {
    li[i].classList.remove('selected');
  }
  li[value].classList.add('selected');

  if (type == 'is_freeze') {
    filter_freeze(value)
  }
}

function filter_freeze(value) {
  switch (value) {
    case 0:
      value = 'zero';
      break;
    case 1:
      value = true;
      break;
    case 2:
      value = false;
      break;
  }
  var tr = document.getElementById("tbody").getElementsByTagName('tr');
  for (var i = 0; i < tr.length; i++) {
    if (value == 'zero' || value == tr[i].getElementsByClassName("freeze")[0].getElementsByClassName("yeees").length) {
      tr[i].classList.remove("hidden-freeze");
    } else {
      tr[i].classList.add("hidden-freeze");
    }
  }
  update_corols();
}

function filter_clear() {
  filter_freeze(0);
}
