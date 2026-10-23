
from openpyxl import load_workbook
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
import pypandoc


def extract_excel_values(
    excel_file,
    txt_file,
    start_cell="G2",
    end_cell="G522",
    increment=5,
    sheet_name=None
):
    """
    Extract values at regular row intervals from an Excel column
    and write them to a text file, one value per line.
    """

    # Open the workbook
    workbook = load_workbook(excel_file, data_only=True)

    # Select the worksheet
    sheet = workbook[sheet_name] if sheet_name else workbook.active

    # Parse the starting and ending cell references
    start_col, start_row = coordinate_from_string(start_cell)
    end_col, end_row = coordinate_from_string(end_cell)

    # Ensure the start and end cells are in the same column
    if start_col != end_col:
        raise ValueError(
            "Starting and ending cells must be in the same column."
        )

    if increment < 1:
        raise ValueError("Increment must be at least 1.")

    # Extract values at the specified interval
    values = []
    for row in range(start_row, end_row + 1, increment):
        value = sheet[f"{start_col}{row}"].value
        values.append("" if value is None else str(value))

    # Write values to the text file
    with open(txt_file, "w", encoding="utf-8") as file:
        file.write("\n".join(values))

    workbook.close()

    print(f"Extracted {len(values)} values to {txt_file}")


def convert_word_to_text(word_file, txt_file):
    """
    Convert a Word document to a plain text file using pypandoc.
    """

    # Convert the Word document to plain text
    text = pypandoc.convert_file(
        word_file,
        to="plain",
        format="docx"
    )

    # Write the extracted text to the output file
    with open(txt_file, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Converted Word document to {txt_file}")


