function show_footer() {
	let	HTMLString = '<p>"I sound my barbaric yawp over the roofs of the world." &mdash;Whitman</p><p>Copyright&copy;2021 exultoshores.com</p>';
    document.getElementById("main_footer").innerHTML = HTMLString;
}

function activate_table_sorting() {
    let asc = true;         // Start ascending as direction
    let last_col_id = -1;   // Track last column clicked
    // Select all the TH elements in the document and listen for clicks on them
    document.querySelectorAll('th').forEach(th => 
        th.addEventListener('click', () => {
            // Click is detected
            // Work on the table element whose header was clicked
            const table = th.closest('table');
            // Make an array containing all the rows except the first (header) row
            let trs = Array.from(table.querySelectorAll('tr:nth-child(n+2)'));
            // Get the values in each row of the selected column
            // tracking the original row number as well
            // in a list of pairs: [[val, row], [val, row], ... ]
            let col_id = Array.from(th.parentNode.children).indexOf(th);
            let valrows = [];
            trs.forEach(tr => {
                let a = [];
                a.push(tr.children[col_id].innerText);   //val of cell
                a.push(tr.rowIndex-1);  //rowIndex starts at 1 not 0
                valrows.push(a);
            });
            // If clicking same column as last time, reverse direction
            if (col_id == last_col_id) { 
                asc = !asc;
            } else {
                // If clicking on new column, direction is ascending
                asc = true;
            };
            last_col_id = col_id;
            // Sort valrows by val depending on direction
            if (asc) {
                valrows = valrows.sort();
            } else {
                // valrows = valrows.reverse(); may fail
                // so use compare function instead
                valrows.sort((a,b) => {
                    if (a < b) {
                        return 1;
                    } else if (a > b) {
                        return -1;
                    return 0;
                    }
                })
            }
            // Create a list of rows in sorted order by rowIndex
            let newtrs = [];
            valrows.forEach(vr => {
                newtrs.push(trs[vr[1]]);
            })
            // Add sorted rows to table, replacing unsorted
            newtrs.forEach(tr => table.appendChild(tr));
        })
    ) 
}