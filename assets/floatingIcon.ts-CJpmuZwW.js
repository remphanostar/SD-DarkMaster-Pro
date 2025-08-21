let l=null,a=null,L="",S=[],v={x:0,y:0},y=null,p=!1,f=!1,k=null;function N(){console.log("Initializing floating icon script"),x(),w();let o=!1;try{o=localStorage.getItem("rcp_highlight_feature_enabled")==="true",console.log("Feature state from localStorage:",o)}catch(t){console.warn("Could not read from localStorage",t)}chrome.storage.local.get("textToPromptEnabled",t=>{f=t.textToPromptEnabled===!0,console.log("Text-to-prompt feature from storage:",f);try{localStorage.setItem("rcp_highlight_feature_enabled",f?"true":"false")}catch(s){console.warn("Could not save to localStorage",s)}f===!0?(console.log("Feature explicitly enabled - attaching selection listeners"),M()):(console.log("Feature disabled or undefined - ensuring complete cleanup"),x(),w(),c())}),setTimeout(()=>{f===void 0&&(console.log("Storage query timed out, falling back to localStorage value"),f=o,f||(x(),w()))},1e3),F(),document.addEventListener("mousemove",t=>{v={x:t.clientX,y:t.clientY}}),chrome.runtime.sendMessage({action:"getFolders"},t=>{t&&t.folders&&(S=t.folders)});function c(){f===!1&&(console.log("Setting up mutation observer to catch any floating icons"),new MutationObserver(s=>{var d;for(const n of s)if(n.type==="childList"){const e=Array.from(n.addedNodes);for(const i of e)i instanceof HTMLElement&&(i.id==="rcp-floating-icon"||i.classList.contains("rcp-floating-icon")||i.querySelectorAll("#rcp-floating-icon, .rcp-floating-icon").length>0)&&(console.log("Found floating icon after feature disabled - removing"),i.id==="rcp-floating-icon"?(d=i.parentNode)==null||d.removeChild(i):i.querySelectorAll("#rcp-floating-icon, .rcp-floating-icon").forEach(u=>{var m;return(m=u.parentNode)==null?void 0:m.removeChild(u)}))}}).observe(document.body,{childList:!0,subtree:!0}))}chrome.runtime.onMessage.addListener((t,s,d)=>{if(t.action==="foldersUpdated")chrome.runtime.sendMessage({action:"getFolders"},n=>{n&&n.folders&&(S=n.folders)});else if(t.action==="themeChanged")p=t.isDarkMode,a&&a.style.display==="flex"&&C();else if(t.action==="textToPromptToggled"){const n=t.timestamp||new Date().getTime();console.log(`Received textToPromptToggled message (${n}): ${t.enabled}`),f=t.enabled===!0,console.log("Performing complete cleanup of floating icon feature"),x(),w(),a&&a.style.display==="flex"&&E();try{localStorage.setItem("rcp_highlight_feature_enabled",f?"true":"false"),sessionStorage.setItem("rcp_highlight_feature_disabled_timestamp",String(Date.now())),console.log("Saved feature state to storage:",f)}catch(e){console.warn("Could not save to storage",e)}f||c(),d({success:!0,newState:f,timestamp:n}),f?(console.log("Re-attaching selection listeners for enabled feature"),M(),D()):console.log("Feature disabled, skipping listener attachment")}}),window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>{F(),a&&a.style.display==="flex"&&C()}),chrome.runtime.sendMessage({action:"getTheme"},t=>{t&&t.hasOwnProperty("isDarkMode")&&(p=t.isDarkMode)}),A()}function M(){console.log("Attaching selection event listeners"),x(),k=function(){y!==null&&window.clearTimeout(y),y=window.setTimeout(D,200)},document.addEventListener("mouseup",B),document.addEventListener("keyup",B),document.addEventListener("selectionchange",k)}function x(){console.log("Detaching selection event listeners"),document.removeEventListener("mouseup",B),document.removeEventListener("keyup",B),k&&(document.removeEventListener("selectionchange",k),k=null),y!==null&&(window.clearTimeout(y),y=null),L=""}function F(){p=window.matchMedia&&window.matchMedia("(prefers-color-scheme: dark)").matches}function A(){const o=document.createElement("style");o.textContent=`
    @keyframes rcp-fade-in {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    @keyframes rcp-fade-out {
      from { opacity: 1; }
      to { opacity: 0; }
    }

    @keyframes rcp-spring-in {
      0% { transform: scale(0.5) translateY(-20px); opacity: 0; }
      60% { transform: scale(1.1); opacity: 1; }
      80% { transform: scale(0.95); }
      100% { transform: scale(1); }
    }
    
    @keyframes rcp-spin {
      0% { transform: rotate(0deg) scale(0.5); opacity: 0; }
      70% { transform: rotate(555deg) scale(1.1); opacity: 1; }
      85% { transform: rotate(540deg) scale(0.95); }
      100% { transform: rotate(540deg) scale(1.0); }
    }

    .rcp-error-field {
      border-color: #EF4444 !important;
    }

    .rcp-error-message {
      color: #EF4444;
      font-size: 12px;
      margin-top: 4px;
      display: block;
    }

    .rcp-btn-primary {
      background-color: #EF4444;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 8px 16px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .rcp-btn-primary:hover {
      background-color: #DC2626;
    }

    .rcp-btn-secondary {
      background-color: #E5E7EB;
      color: #1F2937;
      border: 1px solid #D1D5DB;
      border-radius: 8px;
      padding: 8px 16px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .rcp-btn-secondary:hover {
      background-color: #D1D5DB;
    }

    .rcp-input {
      width: 100%;
      padding: 8px 12px;
      border: 1px solid #D1D5DB;
      border-radius: 8px;
      font-size: 14px;
      box-sizing: border-box;
      transition: border-color 0.2s ease;
      background-color: white;
      color: #1F2937;
    }

    .rcp-input:focus {
      outline: none;
      border-color: #EF4444;
      box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }
    
    .rcp-dark-mode .rcp-btn-primary {
      background-color: #EF4444;
      color: white;
    }
    
    .rcp-dark-mode .rcp-btn-primary:hover {
      background-color: #DC2626;
    }
    
    .rcp-dark-mode .rcp-btn-secondary {
      background-color: #333333;
      border-color: #4B5563;
      color: #D1D5DB;
    }
    
    .rcp-dark-mode .rcp-btn-secondary:hover {
      background-color: #4B5563;
    }
    
    .rcp-dark-mode .rcp-input {
      background-color: #202124;
      border-color: #333333;
      color: #E5E7EB;
    }
    
    .rcp-dark-mode .rcp-input::placeholder {
      color: #9CA3AF;
    }
    
    .rcp-floating-svg {
      filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
      animation: rcp-spin 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
      transform-origin: center;
      width: 48px;
      height: 48px;
    }
  `,document.head.appendChild(o)}function B(o){if(!f){b();return}y!==null&&window.clearTimeout(y),y=window.setTimeout(()=>{D()},200)}function D(){if(!f){b(),x();return}const o=window.getSelection();if(!o||o.toString().trim()===""){b();return}const c=o.toString().trim();c.length>0?(L=c,z()):b()}function z(){if(!f){console.log("Feature is disabled, not showing floating icon"),w();return}try{if(localStorage.getItem("rcp_highlight_feature_enabled")==="false"){console.log("Feature disabled according to localStorage, not showing icon"),w();return}}catch{}b(),l||(l=document.createElement("div"),l.id="rcp-floating-icon",l.innerHTML=`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" class="rcp-floating-svg">
        <!-- White outline around the whole logo (slightly larger) -->
        <polygon points="100,36 155,68 155,132 100,164 45,132 45,68" fill="none" stroke="white" stroke-width="4" />
        
        <!-- White background inside hexagon -->
        <polygon points="100,40 152,70 152,130 100,160 48,130 48,70" fill="white" />
        
        <!-- Outer node white outlines -->
        <circle cx="100" cy="40" r="14" fill="white" stroke="white" stroke-width="3" />
        <circle cx="152" cy="70" r="14" fill="white" stroke="white" stroke-width="3" />
        <circle cx="152" cy="130" r="14" fill="white" stroke="white" stroke-width="3" />
        <circle cx="100" cy="160" r="14" fill="white" stroke="white" stroke-width="3" />
        <circle cx="48" cy="130" r="14" fill="white" stroke="white" stroke-width="3" />
        <circle cx="48" cy="70" r="14" fill="white" stroke="white" stroke-width="3" />
        
        <!-- Lines connecting nodes to center -->
        <line x1="100" y1="100" x2="100" y2="40" stroke="black" stroke-width="5" />
        <line x1="100" y1="100" x2="100" y2="160" stroke="black" stroke-width="5" />
        <line x1="100" y1="100" x2="152" y2="70" stroke="black" stroke-width="5" />
        <line x1="100" y1="100" x2="152" y2="130" stroke="black" stroke-width="5" />
        <line x1="100" y1="100" x2="48" y2="70" stroke="black" stroke-width="5" />
        <line x1="100" y1="100" x2="48" y2="130" stroke="black" stroke-width="5" />
        
        <!-- Outer hexagon connections -->
        <line x1="100" y1="40" x2="152" y2="70" stroke="black" stroke-width="5" />
        <line x1="152" y1="70" x2="152" y2="130" stroke="black" stroke-width="5" />
        <line x1="152" y1="130" x2="100" y2="160" stroke="black" stroke-width="5" />
        <line x1="100" y1="160" x2="48" y2="130" stroke="black" stroke-width="5" />
        <line x1="48" y1="130" x2="48" y2="70" stroke="black" stroke-width="5" />
        <line x1="48" y1="70" x2="100" y2="40" stroke="black" stroke-width="5" />
        
        <!-- Outer nodes (black) -->
        <circle cx="100" cy="40" r="12.5" fill="black" />
        <circle cx="152" cy="70" r="12.5" fill="black" />
        <circle cx="152" cy="130" r="12.5" fill="black" />
        <circle cx="100" cy="160" r="12.5" fill="black" />
        <circle cx="48" cy="130" r="12.5" fill="black" />
        <circle cx="48" cy="70" r="12.5" fill="black" />
        
        <!-- Center node (red) -->
        <circle cx="100" cy="100" r="14.5" fill="#EF4444" stroke="black" stroke-width="5" />
      </svg>
    `,l.style.cssText=`
      position: fixed;
      z-index: 999999999;
      display: block;
      cursor: pointer;
      user-select: none;
      pointer-events: auto;
    `,l.addEventListener("mouseenter",()=>{if(l){const e=l.querySelector(".rcp-floating-svg");e&&(e.classList.add("rcp-hover"),e.style.transform="scale(1.1)")}}),l.addEventListener("mouseleave",()=>{if(l){const e=l.querySelector(".rcp-floating-svg");e&&(e.classList.remove("rcp-hover"),e.style.transform="scale(1)")}}),l.addEventListener("click",e=>{e.preventDefault(),e.stopPropagation(),H()}),document.body.appendChild(l));const o=48,c=10;let r=v.x+c,t=v.y+c;const s=window.innerWidth,d=window.innerHeight;r+o>s&&(r=v.x-o-c),t+o>d&&(t=v.y-o-c),r+=window.scrollX,t+=window.scrollY,l.style.left=`${r}px`,l.style.top=`${t}px`,l.style.display="block";const n=l.querySelector(".rcp-floating-svg");n&&(n.classList.remove("rcp-floating-svg"),n.offsetWidth,n.classList.add("rcp-floating-svg")),setTimeout(()=>{document.addEventListener("click",P),document.addEventListener("scroll",I),window.addEventListener("resize",I)},100)}function I(){l&&l.style.display!=="none"&&(b(),z())}function P(o){l&&!l.contains(o.target)&&b()}function b(){l&&(l.style.display="none",document.removeEventListener("click",P),document.removeEventListener("scroll",I),window.removeEventListener("resize",I))}function w(){b(),l&&l.parentNode&&(l.parentNode.removeChild(l),l=null,console.log("Floating icon completely removed from DOM")),a&&a.parentNode&&(a.parentNode.removeChild(a),a=null,console.log("Modal completely removed from DOM"))}function O(){let o=!0;const c=document.getElementById("rcp-prompt-title"),r=document.getElementById("rcp-title-error");c.value.trim()?(c.classList.remove("rcp-error-field"),r&&(r.style.display="none")):(c.classList.add("rcp-error-field"),r&&(r.style.display="block"),o=!1);const t=document.getElementById("rcp-folder-select"),s=document.getElementById("rcp-folder-error"),d=document.getElementById("rcp-new-folder-container"),n=document.getElementById("rcp-new-folder-name"),e=document.getElementById("rcp-new-folder-error"),i=d&&window.getComputedStyle(d).display!=="none";return!t.value&&(!i||!n.value.trim())?(t.classList.add("rcp-error-field"),s&&(s.style.display="block"),i&&!n.value.trim()&&(n.classList.add("rcp-error-field"),e&&(e.style.display="block")),o=!1):(t.classList.remove("rcp-error-field"),s&&(s.style.display="none"),n&&n.classList.remove("rcp-error-field"),e&&(e.style.display="none")),o}function H(){b(),F(),a||(a=document.createElement("div"),a.id="rcp-modal",a.style.cssText=`
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999999999;
      animation: rcp-fade-in 0.2s ease-in-out;
    `,document.body.appendChild(a)),C(),a.style.display="flex"}function C(){if(!a)return;const o=p?"rcp-dark-mode":"",c=p?"#1A1A1A":"#FFFFFF",r=p?"#333333":"#E5E7EB",t=p?"#E5E7EB":"#111827",s=p?"#D1D5DB":"#374151",d=p?"#FFFFFF":"#111827",n=p?"#202124":"#F9FAFB",e=p?"#D1D5DB":"#4B5563",i=p?"#202124":"#FFFFFF",g=p?"#333333":"#D1D5DB",u=p?"#333333":"#E5E7EB",m=p?"#D1D5DB":"#1F2937";a.innerHTML=`
    <div class="rcp-modal-container ${o}" style="
      background-color: ${c};
      border-radius: 20px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
      width: 500px;
      max-width: 90vw;
      max-height: 90vh;
      overflow: auto;
      padding: 24px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
      color: ${t};
      animation: rcp-fade-in 0.3s ease-out;
    ">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 1px solid ${r}; padding-bottom: 12px;">
        <h2 style="margin: 0; font-size: 18px; font-weight: 600; color: ${d};">Save Prompt</h2>
        <button id="rcp-modal-close" style="
          background: none;
          border: none;
          cursor: pointer;
          font-size: 20px;
          color: ${p?"#9CA3AF":"#6B7280"};
          padding: 4px 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 8px;
          transition: background-color 0.2s;
        ">×</button>
      </div>
      
      <div style="margin-bottom: 16px;">
        <label for="rcp-prompt-title" style="display: block; margin-bottom: 6px; font-weight: 500; color: ${s};">Title <span style="color: #EF4444;">*</span></label>
        <input id="rcp-prompt-title" type="text" placeholder="Enter a title for your prompt" class="rcp-input" style="background-color: ${i}; border-color: ${g};">
        <span id="rcp-title-error" class="rcp-error-message" style="display: none;">Please enter a title for your prompt</span>
      </div>
      
      <div style="margin-bottom: 16px;">
        <label for="rcp-folder-select" style="display: block; margin-bottom: 6px; font-weight: 500; color: ${s};">Folder <span style="color: #EF4444;">*</span></label>
        <div style="display: flex; gap: 8px;">
          <select id="rcp-folder-select" class="rcp-input" style="flex: 1; background-color: ${i}; border-color: ${g}; color: ${t};">
            <option value="">Select a folder</option>
            ${S.map(h=>`<option value="${h.id}">${h.name}</option>`).join("")}
          </select>
          <button id="rcp-new-folder-btn" class="rcp-btn-secondary" style="background-color: ${u}; color: ${m};">New Folder</button>
        </div>
        <span id="rcp-folder-error" class="rcp-error-message" style="display: none;">Please select a folder or create a new one</span>
      </div>
      
      <div id="rcp-new-folder-container" style="display: none; margin-bottom: 16px; padding: 12px; background-color: ${p?"#202124":"#F9FAFB"}; border-radius: 8px; border-left: 3px solid #EF4444;">
        <label for="rcp-new-folder-name" style="display: block; margin-bottom: 6px; font-weight: 500; color: ${s};">New Folder Name <span style="color: #EF4444;">*</span></label>
        <div style="display: flex; gap: 8px;">
          <input id="rcp-new-folder-name" type="text" placeholder="Enter folder name" class="rcp-input" style="flex: 1; background-color: ${i}; border-color: ${g};">
          <button id="rcp-create-folder-btn" class="rcp-btn-primary">Create</button>
        </div>
        <span id="rcp-new-folder-error" class="rcp-error-message" style="display: none;">Please enter a folder name</span>
      </div>
      
      <div style="margin-bottom: 20px;">
        <label for="rcp-prompt-preview" style="display: block; margin-bottom: 6px; font-weight: 500; color: ${s};">Preview</label>
        <div id="rcp-prompt-preview" style="
          width: 100%;
          min-height: 80px;
          max-height: 200px;
          padding: 12px;
          border: 1px solid ${r};
          border-radius: 8px;
          font-size: 14px;
          line-height: 1.5;
          overflow: auto;
          background-color: ${n};
          white-space: pre-wrap;
          box-sizing: border-box;
          color: ${e};
        ">${L}</div>
      </div>
      
      <div style="display: flex; justify-content: flex-end; gap: 12px; margin-top: 8px;">
        <button id="rcp-cancel-btn" class="rcp-btn-secondary" style="background-color: ${u}; color: ${m};">Cancel</button>
        <button id="rcp-save-btn" class="rcp-btn-primary">Save Prompt</button>
      </div>
    </div>
  `,j()}function j(){var r,t,s,d,n;(r=document.getElementById("rcp-modal-close"))==null||r.addEventListener("click",E),(t=document.getElementById("rcp-cancel-btn"))==null||t.addEventListener("click",E),(s=document.getElementById("rcp-new-folder-btn"))==null||s.addEventListener("click",()=>{const e=document.getElementById("rcp-new-folder-container");e&&(e.style.display="block",setTimeout(()=>{const i=document.getElementById("rcp-new-folder-name");i&&i.focus()},100))}),(d=document.getElementById("rcp-create-folder-btn"))==null||d.addEventListener("click",()=>{const e=document.getElementById("rcp-new-folder-name"),i=document.getElementById("rcp-new-folder-error"),g=e.value.trim();if(!g){e.classList.add("rcp-error-field"),i&&(i.style.display="block");return}e.classList.remove("rcp-error-field"),i&&(i.style.display="none"),chrome.runtime.sendMessage({action:"createFolder",name:g},u=>{if(u&&u.success){const m=document.getElementById("rcp-folder-select"),h=document.createElement("option");h.value=u.folderId,h.textContent=g,m.appendChild(h),m.value=u.folderId;const T=document.getElementById("rcp-new-folder-container");T&&(T.style.display="none"),e.value="";const $=document.getElementById("rcp-folder-error");$&&($.style.display="none"),m.classList.remove("rcp-error-field")}})}),(n=document.getElementById("rcp-save-btn"))==null||n.addEventListener("click",()=>{if(!O())return;const e=document.getElementById("rcp-prompt-title"),i=document.getElementById("rcp-folder-select"),g=e.value.trim(),u=i.value;chrome.runtime.sendMessage({action:"savePrompt",title:g,text:L,folderId:u},m=>{m&&m.success?(E(),_("Prompt saved successfully!")):m&&m.error&&_(`Error: ${m.error}`,!0)})});const o=document.getElementById("rcp-prompt-title");o.addEventListener("input",()=>{if(o.value.trim()){o.classList.remove("rcp-error-field");const e=document.getElementById("rcp-title-error");e&&(e.style.display="none")}});const c=document.getElementById("rcp-folder-select");c.addEventListener("change",()=>{if(c.value){c.classList.remove("rcp-error-field");const e=document.getElementById("rcp-folder-error");e&&(e.style.display="none")}}),setTimeout(()=>{const e=document.getElementById("rcp-prompt-title");e&&e.focus()},100)}function E(){a&&(a.style.display="none")}function _(o,c=!1){F();const r=document.createElement("div"),t="#2D2D2D",s="#EF4444";r.style.cssText=`
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background-color: ${t};
    color: white;
    padding: 10px 16px;
    border-radius: 8px;
    border-left: 4px solid ${s};
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 999999999;
    min-width: 200px;
    max-width: 80%;
    display: flex;
    align-items: center;
    gap: 8px;
    animation: rcp-fade-in 0.2s ease-in-out;
  `;const d=document.createElement("span");c?d.innerHTML=`
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="15" y1="9" x2="9" y2="15"></line>
        <line x1="9" y1="9" x2="15" y2="15"></line>
      </svg>
    `:d.innerHTML=`
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
    `;const n=document.createElement("span");n.textContent=o,r.appendChild(d),r.appendChild(n),document.body.appendChild(r),setTimeout(()=>{r.style.opacity="0",r.style.transform="translate(-50%, -10px)",r.style.transition="opacity 0.3s ease-out, transform 0.3s ease-out",setTimeout(()=>{document.body.contains(r)&&document.body.removeChild(r)},300)},3e3)}(function(){(()=>{console.log("Pre-initialization cleanup");try{localStorage.getItem("rcp_highlight_feature_enabled")==="false"&&(console.log("Feature known to be disabled, performing immediate cleanup"),document.querySelectorAll("#rcp-floating-icon, .rcp-floating-icon").forEach(r=>{r.parentNode&&(r.parentNode.removeChild(r),console.log("Removed existing icon during pre-init"))}))}catch{}})(),N()})();
//# sourceMappingURL=floatingIcon.ts-CJpmuZwW.js.map
