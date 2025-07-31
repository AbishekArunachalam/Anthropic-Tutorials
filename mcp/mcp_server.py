from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
        name="read_doc",
        description ="Reads the content of a document and return it as a string."
)
def read_document(doc_id: str = Field(description="The ID of the document to read.")) -> str:
    """
    Reads the content of a document by its ID.
    
    Args:
        doc_id (str): The ID of the document to read.
    
    Returns:
        str: The content of the document.
    """
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    return docs.get(doc_id)


@mcp.tool(
    name="edit_doc",
    description="Edits the content of a document by its ID and replaces the old content with new content."
)
def edit_document(doc_id: str = Field(description="The ID of the document to edit."),
                   new_content: str = Field(description="The new content to replace the old content.")) -> str:
    """
    Edits the content of a document by its ID.
    
    Args:
        doc_id (str): The ID of the document to edit.
        new_content (str): The new content to replace the old content.
    
    Returns:
        str: A message indicating the result of the edit operation.
    """
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    docs[doc_id] = new_content


@mcp.resource(
        "docs://documents",
        mime_type="application/json"
)
def list_docs() -> list[str]:
    """
    Returns a list of all document IDs.
    
    Returns:
        list[str]: A list of document IDs.
    """
    return list(docs.keys())


@mcp.resource(
        "docs://documents/{doc_id}",
        mime_type="text/plain"
)
def get_doc_content(doc_id: str) -> str:
    """
    Returns the content of a document by its ID.

    Args:
        doc_id (str): The ID of the document to retrieve.

    Returns:
        str: The content of the document.
    """
    if doc_id not in docs:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    return docs.get(doc_id)


@mcp.prompt(name = "format",
            description = "Formats a document in markdown format."
)
def format_document(
    doc_id: str = Field(description="The ID of the document to format.")
) -> list[base.Message]:
    """    
    Formats a document in markdown format.
    
    Args:
        doc_id (str): The ID of the document to format.
    
    Returns:
        list[base.Message]: A list containing a UserMessage with the formatting instructions.
    """
    prompt = f"""
    Your goal is to reformat a document to be written with markdown syntax.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [base.UserMessage(content=prompt)]

# # TODO: Write a prompt to summarize a doc
# @mcp.prompt("summarize_doc")
# def summarize_doc(doc_id: str) -> str:
#     """
#     Summarizes a document by its ID.

#     Args:
#         doc_id (str): The ID of the document to summarize.

#     Returns:
#         str: The summary of the document.
#     """
#     content = docs.get(doc_id, "Document not found.")
#     return f"Summary of {doc_id}: {content[:100]}..."
    """
    return docs.get(doc_id, "Document not found.")

# # TODO: Write a resource to return the contents of a particular doc
# @mcp.resource("doc_content")
# def get_doc_content(doc_id: str) -> str:
#     """
#     Returns the content of a document by its ID.
    
#     Args:
#         doc_id (str): The ID of the document to retrieve.
    
#     Returns:
#         str: The content of the document.
#     """
#     return docs.get(doc_id, "Document not found.")

# # TODO: Write a prompt to rewrite a doc in markdown format
# @mcp.prompt("rewrite_doc")
# def rewrite_doc(doc_id: str) -> str:
#     """
#     Rewrites a document in markdown format.
    
#     Args:
#         doc_id (str): The ID of the document to rewrite.
    
#     Returns:
#         str: The rewritten document in markdown format.
#     """
#     content = docs.get(doc_id, "Document not found.")
#     return f"# {doc_id}\n\n{content}"

# # TODO: Write a prompt to summarize a doc
# @mcp.prompt("summarize_doc")
# def summarize_doc(doc_id: str) -> str:
#     """
#     Summarizes a document by its ID.
    
#     Args:
#         doc_id (str): The ID of the document to summarize.
    
#     Returns:
#         str: The summary of the document.
#     """
#     content = docs.get(doc_id, "Document not found.")
#     return f"Summary of {doc_id}: {content[:100]}..."


if __name__ == "__main__":
    mcp.run(transport="stdio")
