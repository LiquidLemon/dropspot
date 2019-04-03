let qr = qrcode(0, "L");
let url = document.getElementById("noscript-qr-url").innerText.trim();
qr.addData(url);
qr.make();
document.getElementById("qr-placeholder").innerHTML = qr.createImgTag(5);