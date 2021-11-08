
function changeIframeUrl(){
	const inputBar = document.querySelector("#inputBar").value;
    document.getElementById("main_frame").src = "https://www.youtube.com/embed/"+inputBar;
}

// <iframe src="http://34.133.131.183/d-solo/aws/aws?orgId=1&refresh=5s&theme=light&panelId=145" width="450" height="200" frameborder="0"></iframe>

// "아이피/d-solo/UID/대시보드이름?orgId=1&refresh=10s&theme=light&panelId=164"