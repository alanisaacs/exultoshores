// JavaScript for all sites

// Framework

function showPageFooter() {
	let	HTMLString = '<p>"I sound my barbaric yawp over the roofs of the world." &mdash;Whitman</p><p>Copyright&copy;2021 exultoshores.com</p>';
    document.getElementById("pageFooter").innerHTML = HTMLString;
}

// Tables

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
                //val of cell at a[0]; sort will be case insensitive
                a.push(tr.children[col_id].innerText.toLowerCase());
                //rowIndex at a[1]; minus one because rowIndex starts at 1
                a.push(tr.rowIndex-1); 
                valrows.push(a);
            });
            // If clicking same column as last time, reverse direction
            // If clicking on new column, direction is ascending
            asc = (col_id == last_col_id) ? !asc : true;
            last_col_id = col_id;
            // Sort valrows by val depending on direction
            // a & b are each a list, [val, row]
            valrows.sort((a,b) => {
                let x = a[0];
                let y = b[0];
                // If comparing numbers, just subtract
                if (!isNaN(x) && !isNaN(y) && x != '' && y != '') {
                    return asc ? x - y : y - x;
                // Also have blank strings sort after chars
                } else if (x > y || x == '') {
                    return asc ? 1 : -1;
                } else if (x < y || y == '') {
                    return asc ? -1 : 1;
                }
                return 0;
                });
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

// Text

// Find certain characters user can enter as markup
// and convert them to UTF-8 characters or html tags
function convertUserMarkup(text) {
	let s = text;
	if (s) {    // Avoid errors when text is null
        // Treat underscores around words as <em> tags
		// Replace space+underscore+character
		s = s.replace(/(\s)_(\w)/g, '$1<em>$2');
		// Replace character+underscore+space/punctuation
		s = s.replace(/(\w)_([\s,.;&)<])/g, '$1</em>$2');
        // Replace double hyphens with em dashes
        s = s.replace(/--/g, '—')
	}
	return s;
}