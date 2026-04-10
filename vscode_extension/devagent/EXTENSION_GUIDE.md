# DevAgent Extension - Setup & Testing Guide

## ✅ How to Run the Extension

### Option 1: Quick Debug Launch (Recommended)
1. Open the `devagent` folder in VS Code
2. Press **F5** (or go to `Run > Start Debugging`)
3. This opens a new VS Code window with DevAgent loaded
4. Look for the **rocket icon** in the Activity Bar (left sidebar)
5. Click it to see your Chat interface

### Option 2: Command Line
```powershell
cd d:\devagent\vscode_extension\devagent
code --extensionDevelopmentPath=.
```

---

## 🧪 What to Test

### 1. **Icon Visibility**
- [ ] Rocket icon visible in Activity Bar (left side)
- [ ] Icon is colorful and distinct

### 2. **Chat View**
- [ ] Click the rocket icon
- [ ] "Chat" sidebar appears
- [ ] Input box and chat area visible

### 3. **Functionality**
- [ ] Type a message in the input field
- [ ] Press Enter
- [ ] Message appears in chat as "You:"
- [ ] Response appears as "DevAgent:"

### 4. **Expected Response**
Input: "Hello"
Expected: _"You said: "Hello". My Python brain connection is coming next!"_

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Icon doesn't appear | Reload window (Ctrl+R) in debug session |
| Chat sidebar missing | Click rocket icon in Activity Bar |
| No response | Check DevTools (Help > Toggle Developer Tools) |
| Extension won't launch | Run `npm run compile` first, then F5 |

---

## 📝 Project Files
- **Extension code**: `src/extension.ts`
- **Icon**: `resources/icon.svg`
- **Config**: `package.json`
- **Compiled output**: `out/extension.js`

---

## Next Steps
After testing, you can:
1. Connect to your Python FastAPI backend
2. Add more chat features
3. Package as `.vsix` for distribution

**Enjoy your DevAgent! 🚀**
