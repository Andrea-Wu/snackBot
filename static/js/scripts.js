let lolArray = [];


const makeStar = (num) => {
	Document.getElementById("starField").innerHTML += "*";
	lolArray.push(num);
}

const submitPin = () =>{
	let i;
	let pin = "";

	for(i = 0; i < lolArray.length; i++){
		pin += lolArray[i];
	}

	//sends POST to server
	$.ajax({
		url: "placeholder_url",
		type: "POST",
		data: pin,
	});

	lolArray = [];
	Document.getElementById("starField").innerHTML = "";

}

