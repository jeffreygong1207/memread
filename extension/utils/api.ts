export const API_URL = 'http://localhost:8000/v1';

export async function ingestChat(payload: any) {
  try {
    const response = await fetch(`${API_URL}/ingest`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to ingest chat:', error);
    throw error;
  }
}

export async function fetchContext(query: string) {
  try {
    const response = await fetch(`${API_URL}/context?query=${encodeURIComponent(query)}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch context:', error);
    return { context: [] };
  }
}
