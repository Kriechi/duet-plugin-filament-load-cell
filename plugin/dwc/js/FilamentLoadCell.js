(window["webpackJsonp"] = window["webpackJsonp"] || []).push([
    ["FilamentLoadCell"], {
        "./src/plugins/FilamentLoadCell/index.js": function (e, t, n) {
            "use strict";

            var valueEl = document.createElement('span');
            valueEl.id = "load_cell";
            valueEl.className = "ml-2";
            valueEl.innerHTML = "(no weight reading yet)";
            var newEl = document.createElement('div');
            newEl.appendChild(valueEl);

            var ref = document.querySelector('div.v-toolbar__title');
            ref.parentNode.insertBefore(newEl, ref.nextSibling);

            function getUpdate() {
                var xhttp = new XMLHttpRequest();
                xhttp.open("GET", "/machine/filament-load-cell/reading", true);
                xhttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        document.getElementById("load_cell").innerHTML = this.responseText;
                    }
                };;
                xhttp.send();
            }

            window.setInterval(getUpdate, 5000);
            getUpdate();
        }
    }
]);
