function copy(object){
	return JSON.parse(JSON.stringify(object))
}
function print(object){// override default print
	// console.log( new Error().stack )
	console.log(copy(object))
}


function argmax(array){
	return array.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1]
}
function len(array){
	return array.length
}
function sum(array){
	return array.reduce((a, b) => a + b, 0)
}
function count(array,number){
	return array.filter((a) => a == number).length
}
function isNumeric(n) {
	return !isNaN(parseFloat(n)) && isFinite(n);
}
function int(n){
	return Math.floor(n)
}
function str(o){
	return JSON.stringify(o)
}

function concatenate(arr1,arr2){
	return arr1.concat(arr2)
}
function removeFromArray(array,obj){
	var index = array.indexOf(obj);
	if (index > -1) {
		array.splice(index, 1);
	}
}

function operationWithArrays(i_a1,a2,op){
	let a1 = copy(i_a1)
	if (Array.isArray(a2)){
		for (let i = 0; i < a1.length; i++) {
			if (op == "*"){
				a1[i] = a1[i] * a2[i]	
			} else if (op == "+"){
				a1[i] = a1[i] + a2[i]
			}
		}
	} else if (isNumeric(a2)){
		for (let i = 0; i < a1.length; i++) {
			if (op == "*"){
				a1[i] = a1[i] * a2	
			} else if (op == "/"){
				a1[i] = a1[i] / a2
			}
		}
	}
	return a1
}

function operationWith2DArray(i_array2D,number,op){
	let array2D = copy(i_array2D)
	for (let array of array2D) {
		for (let i = 0; i < array.length; i++) {
			if (op == "*"){
				array[i] = array[i] * number	
			} 
		}
	}
	return array2D
}


function range(start,stop){
    if (stop == undefined)
        return [...Array(start).keys()]
    else
        return [...Array(stop - start).keys()].map(i => i + start)
}


function zeros2D(w,h){
	let result = Array(w)
	for (let i of range(w)){
		result[i] = Array(h).fill(0)
	}
	return result
}



// none to number encoder
const NONE_NUMBER = 255
function array_to_array_without_none(array,shape){
	result = zeros2D(shape[0], shape[1])
	for (const [i, number] of array.entries()){
		if (number == null)
			result[i][0] = NONE_NUMBER
		else
			result[i][0] = number
	}
	return result
}

function array_without_none_to_array(array){
	result = []
	for (const [i, number] of array.entries()){
		if (number[0] == NONE_NUMBER)
			result.push(null)
		else
			result.push(int(number[0]))
	}
	return result
}

function number_to_number_without_none(number,array_size){
	return number != null ? [number] : [NONE_NUMBER]
}

function number_without_none_to_number(number){
	number = int(number[0])
	return number != NONE_NUMBER ? number : null
}