from googleapiclient.discovery import build
from auth import get_credentials

def append_to_doc(doc_id: str, content: str) -> dict:
    creds = get_credentials()
    service = build('docs', 'v1', credentials=creds)

    document = service.documents().get(documentId=doc_id).execute()
    content_elements = document.get('body').get('content')
    
    # The last element is a Paragraph, and we want to insert before the last newline
    end_index = content_elements[-1].get('endIndex') - 1
    
    requests = [
        {
            'insertText': {
                'location': {
                    'index': end_index,
                },
                'text': content + "\n"
            }
        }
    ]

    # Execute the request
    result = service.documents().batchUpdate(
        documentId=doc_id, body={'requests': requests}).execute()
    
    return {"status": "success"}
