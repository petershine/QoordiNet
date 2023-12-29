document.addEventListener('DOMContentLoaded', function() {
    var tables = document.getElementsByClassName('csv_table');
    if (tables.length === 0) {
        console.error('Table elements with the class "csv_table" not found');
        return;
    }

    var table = tables[0]; // Assuming you want to work with the first table with class "csv_table"
    var isDragging = false;
    var startCell = { row: null, col: null };
    var currentCell = { row: null, col: null };

    table.addEventListener('mousedown', function(e) {
        var cell = e.target.closest('td');
        if (cell) {
            clearSelection();
            isDragging = true;
            startCell.row = cell.parentElement.rowIndex;
            startCell.col = cell.cellIndex;
            e.preventDefault();
        }
    });

    table.addEventListener('mouseup', function() {
        isDragging = false;
    });

    table.addEventListener('mousemove', function(e) {
        if (!isDragging) return;

        var cell = e.target.closest('td');
        if (cell) {
            currentCell.row = cell.parentElement.rowIndex;
            currentCell.col = cell.cellIndex;
            highlightBox(startCell, currentCell);
        }
    });

    document.addEventListener('click', function(e) {
        if (e.target.closest('.csv_table') === null) {
            clearSelection();
        }
    });

    document.addEventListener('copy', function(e) {
        var selectedCells = table.querySelectorAll('.selected');
        if (selectedCells.length) {
            e.preventDefault(); // Prevent default copy action
            var copyText = getSelectedDataAsTSV(selectedCells);
            e.clipboardData.setData('text/plain', copyText);
        }
    });

    function highlightBox(start, end) {
        clearSelection();
        var minRow = Math.min(start.row, end.row);
        var maxRow = Math.max(start.row, end.row);
        var minCol = Math.min(start.col, end.col);
        var maxCol = Math.max(start.col, end.col);

        for (var i = minRow; i <= maxRow; i++) {
            var row = table.rows[i];
            for (var j = minCol; j <= maxCol; j++) {
                var cell = row.cells[j];
                if (cell) {
                    cell.classList.add('selected');
                }
            }
        }
    }

    function clearSelection() {
        var selectedCells = table.querySelectorAll('.selected');
        selectedCells.forEach(function(cell) {
            cell.classList.remove('selected');
        });
    }

    function getSelectedDataAsTSV(selectedCells) {
        // Collect data from selected cells and format it as tab-separated values
        var rows = new Map();
        selectedCells.forEach(cell => {
            var rowIndex = cell.parentElement.rowIndex;
            var cellIndex = cell.cellIndex;
            if (!rows.has(rowIndex)) {
                rows.set(rowIndex, []);
            }
            rows.get(rowIndex)[cellIndex] = cell.textContent || cell.innerText;
        });

        var tsvData = Array.from(rows, ([, cols]) => cols.join('\t')).join('\n');
        return tsvData;
    }
});
