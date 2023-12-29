

document.addEventListener('DOMContentLoaded', function() {
    var table = document.getElementById('csv_table');
    var isMouseDown = false;
    var startColIndex = null;

    table.addEventListener('mousedown', function(e) {
        isMouseDown = true;
        var cell = e.target.closest('td');
        startColIndex = cell.cellIndex;
        selectColumn(startColIndex);
        e.preventDefault();
    });

    table.addEventListener('mouseup', function() {
        isMouseDown = false;
        startColIndex = null;
    });

    table.addEventListener('mouseover', function(e) {
        if (isMouseDown) {
            var cell = e.target.closest('td');
            selectColumn(cell.cellIndex);
        }
    });

    function selectColumn(colIndex) {
        Array.from(table.rows).forEach(row => {
            var cell = row.cells[colIndex];
            if (cell) {
                cell.classList.add('selected');
            }
        });
    }
});
