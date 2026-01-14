import { useState } from 'react';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ padding: '20px', width: '300px', fontFamily: 'sans-serif' }}>
      <h2>MemRead</h2>
      <p>Status: <span style={{ color: 'green' }}>Active</span></p>
      <p>Memories Synced: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>
        Sync Now
      </button>
    </div>
  );
}

export default App;
