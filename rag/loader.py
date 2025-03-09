class DocumentLoader:
    """
    Utilities for loading financial documents.
    """
    
    def __init__(self):
        self.supported_formats = ["pdf", "txt", "html"]
        
    def load_document(self, file_path):
        """
        Load a document from the specified path.
        
        Args:
            file_path (str): Path to the document
            
        Returns:
            dict: Loaded document data
        """
        # TODO: Implement document loading
        return {"content": "Document content", "metadata": {"source": file_path}}
        
    def load_sec_filing(self, filing_id):
        """
        Load an SEC filing by ID.
        
        Args:
            filing_id (str): The SEC filing ID
            
        Returns:
            dict: Loaded filing data
        """
        # TODO: Implement SEC filing loading
        return {"content": f"Filing {filing_id} content", "metadata": {"id": filing_id}} 