let lolArray = [];


const makeStar = (num) => {
	document.getElementById("starField").innerHTML += "*";
	lolArray.push(num);
}

const submitPin = () =>{
	let i;
	let pin = "";

	for(i = 0; i < lolArray.length; i++){
		pin += lolArray[i];
	}
	console.log(pin);
	//sends POST to server
	$.ajax({
		contentType: "text/plain; charset=utf-8",
		url: "check-pin",
		type: "POST",
		data: pin,
	});

	lolArray = [];
	document.getElementById("starField").innerHTML = "";

}

