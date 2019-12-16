var task = "";

var tasks = document.getElementsByTagName("select");
for (var i = 0; i < tasks.length; i++) {
    tasks[i].addEventListener("change", function() {
        for (var j = 0; j < tasks.length; j++) {
            if (tasks[j].id == this.id) continue;
            tasks[j].selectedIndex = 0;
        }
        task = this.value;

    });
}