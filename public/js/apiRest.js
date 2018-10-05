function setupApi(){return Promise.resolve()}

function predictAction(data){
	return post("/api/predict/", data)
}

function getNextState(data){
	return post("/api/next_state/", data)
}


// network
function post(url,data){
	return new Promise(function(resolve, reject) {
		var xhr = new XMLHttpRequest();
		xhr.open("POST", url, true);
		xhr.setRequestHeader("Content-Type", "application/json");
		xhr.onreadystatechange = function () {
			if (xhr.readyState === 4 && xhr.status === 200) {
				var json = JSON.parse(xhr.responseText);
				resolve(json);
			} else {
				if (!(xhr.status === 200)){
					reject(xhr)
				}
			}
		};
		var strData = JSON.stringify(data);
		xhr.send(strData);

	})
}