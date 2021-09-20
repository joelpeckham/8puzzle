class Table:
    def __init__(self):
        self.title = None
        self.columnNames = [] #Example: ["Column 0 Name", "Column 1 Name", "Column 2 Name"]
        self.rows = [] #Example: [["Row 0 Column 0 Value", "Row 0 Column 1 Value", "Row 0 Column 2 Value"], ["Row 1 Column 0 Value", "Row 1 Column 1 Value", "Row 1 Column 2 Value"]]
    def add_row(self, rowValues):
        self.rows.append(rowValues)
    def add_column(self, columnName, columnValues):
        self.columnNames.append(columnName)
        for i, newValue in enumerate(columnValues):
            newRow = []
            for j in range(len(self.columnNames)):
                if j == i:
                    newRow.append(newValue)
                else:
                    newRow.append(self.rows[j][i])
            self.rows.append(newRow)
    def sort(self, columnIndex, reverse=False):
        """
        Sort the table by the values in the given column.
        """
        self.rows.sort(key=lambda row: row[columnIndex], reverse=reverse)

    def __str__(self):
        # Get the width of each column
        columnWidths = [max(len(self.columnNames[col]),max([len(str(self.rows[row][col])) for row in range(len(self.rows))])) for col in range(len(self.columnNames))]
        # Get the width of the table
        tableWidth = sum(columnWidths) + (len(columnWidths) - 1) * 2
        #Make the top of the table
        top = "┌"+"┬".join(["─"*(columnWidth +2 )for columnWidth in columnWidths])+"┐"
        titleTop = "┌"+"─".join(["─"*(columnWidth +2 )for columnWidth in columnWidths])+"┐"
        # Make header row
        headerRow = "│ " + " │ ".join([self.columnNames[i].ljust(columnWidths[i]) for i in range(len(self.columnNames))]) + " │"
        # Make divider row
        dividerRow = "├"+"┼".join(["─"*(columnWidth+2) for columnWidth in columnWidths])+"┤"
        betweenTableAndTitle = "├"+"┬".join(["─"*(columnWidth +2 )for columnWidth in columnWidths])+"┤"
        # Make bottom row
        bottom = "└"+"┴".join(["─"*(columnWidth+2) for columnWidth in columnWidths])+"┘"
        # Make the table
        if not self.title:
            table = top + "\n" + headerRow + "\n" + dividerRow + "\n"
        else:
            titleRow = f"│{self.title.center(tableWidth+len(columnWidths)+1)}│"
            table = titleTop + "\n" + titleRow + '\n' + betweenTableAndTitle +'\n'+ headerRow + "\n" + dividerRow + "\n"
        
        for row in self.rows:
            table += "│ " + " │ ".join([str(row[i]).ljust(columnWidths[i]) for i in range(len(row))]) + " │\n"
        table += bottom
        return table

def prettyPuzzle(puzzle):
    """
    Prints the puzzle as a 3x3 grid with unicode box drawing characters as an outline. 
    """
    # Convert the puzzle string to a list
    puzzle_list = list(puzzle.replace("-", "◼"))
    output = ""
    output += "┌───────┐\n"
    output += "│ " + " ".join(puzzle_list[:3])  + " │\n"
    output += "│ " + " ".join(puzzle_list[3:6]) + " │\n"
    output += "│ " + " ".join(puzzle_list[6:])  + " │\n"
    output += "└───────┘"
    return output


import math
def progressBarString(barWidth, progressPercent):
    """
    Returns a string of a progress bar with the given width and percent.
    """
    barPieces = ["","▏","▎","▍","▌","▋","▊","▉"]
    barProgress = round(progressPercent/100*barWidth*8)
    bar = "█"*math.floor(barProgress/8) + barPieces[barProgress%8]
    return "["+ bar.ljust(barWidth) + "]"