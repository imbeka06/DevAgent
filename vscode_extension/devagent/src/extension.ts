import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('DevAgent is now active!');

    const provider = new DevAgentChatViewProvider(context.extensionUri);

    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(DevAgentChatViewProvider.viewType, provider)
    );
}

class DevAgentChatViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'devagent.chatView';

    constructor(
        private readonly _extensionUri: vscode.Uri,
    ) { }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri]
        };

        webviewView.webview.html = this._getHtmlForWebview();

        // Handle messages from the webview UI
        webviewView.webview.onDidReceiveMessage(async data => {
            switch (data.type) {
                case 'askAgent':
                    {
                        // Right now, it just echoes back. Next, we connect this to FastAPI!
                        vscode.window.showInformationMessage(`DevAgent heard: ${data.value}`);
                        
                        webviewView.webview.postMessage({ 
                            type: 'response', 
                            value: `You said: "${data.value}". My Python brain connection is coming next!` 
                        });
                        break;
                    }
            }
        });
    }

    private _getHtmlForWebview() {
        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DevAgent</title>
            <style>
                body { font-family: var(--vscode-font-family); padding: 10px; display: flex; flex-direction: column; height: 100vh; box-sizing: border-box; }
                #chat-box { flex-grow: 1; overflow-y: auto; border: 1px solid var(--vscode-panel-border); margin-bottom: 10px; padding: 10px; border-radius: 4px; background: var(--vscode-editor-background); }
                .message { margin-bottom: 12px; line-height: 1.4; }
                .user { color: var(--vscode-terminal-ansiCyan); }
                .agent { color: var(--vscode-terminal-ansiGreen); }
                input { width: 100%; padding: 10px; box-sizing: border-box; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); border-radius: 4px; outline: none; }
                input:focus { border-color: var(--vscode-focusBorder); }
            </style>
        </head>
        <body>
            <h2 style="margin-top: 0; font-size: 16px;">DevAgent Assistant</h2>
            <div id="chat-box"></div>
            <input type="text" id="user-input" placeholder="Ask DevAgent to refactor, debug, or explain..." />

            <script>
                const vscode = acquireVsCodeApi();
                const input = document.getElementById('user-input');
                const chatBox = document.getElementById('chat-box');

                input.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && input.value) {
                        const text = input.value;
                        chatBox.innerHTML += \`<div class="message user"><b>You:</b> <br>\${text}</div>\`;
                        vscode.postMessage({ type: 'askAgent', value: text });
                        input.value = '';
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                });

                window.addEventListener('message', event => {
                    const message = event.data;
                    if (message.type === 'response') {
                        chatBox.innerHTML += \`<div class="message agent"><b>DevAgent:</b> <br>\${message.value}</div>\`;
                        chatBox.scrollTop = chatBox.scrollHeight;
                    }
                });
            </script>
        </body>
        </html>`;
    }
}

export function deactivate() {}