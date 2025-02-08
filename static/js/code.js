// Initialize CodeMirror
let editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
    mode: "javascript", // default mode, can be changed
    theme: "cyberpunk",
    lineNumbers: true,
    autoCloseBrackets: true,
    matchBrackets: true,
    indentUnit: 4,
    tabSize: 4,
    lineWrapping: true,
    extraKeys: {
        "Ctrl-Space": "autocomplete"
    },
    cursorBlinkRate: 530, // Faster cursor blink for that hacker feel
});

// Function to format the AI response with markdown-like syntax
function formatAIResponse(response) {
    // Replace code blocks
    response = response.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    
    // Replace numbered lists
    response = response.replace(/^\d+\.\s+(.*?)$/gm, '<li>$1</li>');
    
    // Add line breaks for readability
    response = response.replace(/\n/g, '<br>');
    
    return response;
}

// Function to send content to backend
async function sendToBackend() {
    const editorContent = editor.getValue();
    const selectedText = editor.getSelection();
    
    try {
        // Show loading state
        document.getElementById('serverResponse').innerHTML = 'Analyzing code...';
        
        const response = await fetch('/api/code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content: editorContent,
                selectedText: selectedText
            })
        });

        const data = await response.json();
        
        if (data.success) {
            document.getElementById('serverResponse').innerHTML = formatAIResponse(data.analysis);
        } else {
            document.getElementById('serverResponse').innerHTML = `Error: ${data.error}`;
        }
    } catch (error) {
        document.getElementById('serverResponse').innerHTML = `Error: ${error.message}`;
    }
}

// Function to change editor mode
function changeEditorMode(mode) {
    editor.setOption("mode", mode);
}

// Chat functionality
function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (!message) return;

    const chatBody = document.getElementById('chat-body');
    chatBody.innerHTML += `<div class="user-message">${message}</div>`;
    input.value = '';

    // Add your chat API call here
}