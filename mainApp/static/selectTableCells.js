document.addEventListener('DOMContentLoaded', function() {
    var tables = document.getElementsByClassName('qoordinet_table');
    if (tables.length === 0) {
        console.error('Table elements with the class "qoordinet_table" not found');
        return;
    }

    var table = tables[0]; // Assuming you want to work with the first table with class "qoordinet_table"
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
        if (e.target.closest('.qoordinet_table') === null) {
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
        // Create a map to hold the data with row and column indices as keys
        let dataMap = new Map();
    
        selectedCells.forEach(cell => {
            var rowIndex = cell.parentElement.rowIndex;
            var colIndex = cell.cellIndex;
            if (!dataMap.has(rowIndex)) {
                dataMap.set(rowIndex, new Map());
            }
            dataMap.get(rowIndex).set(colIndex, cell.textContent || cell.innerText);
        });
    
        // Find the min and max column indices
        let minCol = Infinity, maxCol = -Infinity;
        dataMap.forEach((colMap, _) => {
            Array.from(colMap.keys()).forEach(colIndex => {
                if (colIndex < minCol) minCol = colIndex;
                if (colIndex > maxCol) maxCol = colIndex;
            });
        });
    
        // Construct the TSV data
        let tsvData = [];
        Array.from(dataMap.keys()).sort().forEach(rowIndex => {
            let rowData = [];
            for (let colIndex = minCol; colIndex <= maxCol; colIndex++) {
                rowData.push(dataMap.get(rowIndex).get(colIndex) || '');
            }
            tsvData.push(rowData.join('\t'));
        });
    
        return tsvData.join('\n');
    }
});
