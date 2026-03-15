(function () {

    const icon = document.createElement("div");
    
    icon.style.position = "fixed";
    icon.style.bottom = "20px";
    icon.style.right = "20px";
    icon.style.width = "60px";
    icon.style.height = "60px";
    icon.style.background = "#6878D6";
    icon.style.borderRadius = "50%";
    icon.style.display = "flex";
    icon.style.alignItems = "center";
    icon.style.justifyContent = "center";
    icon.style.cursor = "pointer";
    icon.style.boxShadow = "0 4px 10px rgba(0,0,0,0.3)";
    icon.style.color = "white";
    icon.style.fontSize = "26px";
    
    icon.innerHTML = `
<svg width="26" height="26" viewBox="0 0 24 24" fill="white">
<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"/>
</svg>
`;
    
    const iframe = document.createElement("iframe");
    
    iframe.src = "./chat.html";
    iframe.style.position = "fixed";
    iframe.style.bottom = "90px";
    iframe.style.right = "20px";
    iframe.style.width = "350px";
    iframe.style.height = "500px";
    iframe.style.border = "none";
    iframe.style.display = "none";
    iframe.style.borderRadius = "12px";
    iframe.style.boxShadow = "0 4px 20px rgba(0,0,0,0.3)";
    
    icon.onclick = function () {
    
    iframe.style.display =
    iframe.style.display === "none" ? "block" : "none";
    
    };
    
    document.body.appendChild(icon);
    document.body.appendChild(iframe);
    
    })();