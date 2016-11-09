
alert = print
 var br = new java.io.BufferedReader(new java.io.InputStreamReader(java.lang.System["in"]) );
function prompt(s)
{
	print (s)
    return br.readLine();
};


function num2Letters(number) {

    if (isNaN(number) || number < 0 || 999 < number) {
        return 'Veuillez entrer un nombre entier compris entre 0 et 999.';
    }

    var units2Letters = ['', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize', 'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf'],
        tens2Letters  = ['', 'dix', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante', 'quatre-vingt', 'quatre-vingt'];

    var units    = number % 10,
        tens     = (number % 100 - units) / 10,
        hundreds = (number % 1000 - number % 100) / 100;

    var unitsOut, tensOut, hundredsOut;


    if (number === 0) {

        return 'zero';

    } else {

        // Traitement des unites

        unitsOut = (units === 1 && tens > 0 && tens !== 8 ? 'et-' : '') + units2Letters[units];

        // Traitement des dizaines

        if (tens === 1 && units > 0) {

            tensOut = units2Letters[10 + units];
            unitsOut = '';

        } else if (tens === 7 || tens === 9) {

            tensOut = tens2Letters[tens] +'-'+ (tens === 7 && units === 1 ? 'et-' : '') + units2Letters[10 + units];
            unitsOut = '';

        } else {

            tensOut = tens2Letters[tens];

        }

        tensOut += (units === 0 && tens === 8 ? 's' : '');

        // Traitement des centaines

        hundredsOut = (hundreds > 1 ? units2Letters[hundreds] + '-' : '') + (hundreds > 0 ? 'cent' : '') + (hundreds > 1 && tens == 0 && units == 0 ? 's' : '');

        // Retour du total
  //      tt = hundredsOut * ((hundredsOut && tensOut ? '-': '')) * tensOut  //+ (hundredsOut && unitsOut || tensOut && unitsOut ? '-': '') + unitsOut;
    //    return (hundredsOut && tensOut ? '-': '') 
        return hundredsOut + (hundredsOut && tensOut ? '-': '') + tensOut + (hundredsOut && unitsOut || tensOut && unitsOut ? '-': '') + unitsOut;
    }

}



var userEntry;

while (userEntry = prompt('Indiquez le nombre a ecrire en toutes lettres (entre 0 et 999) :')) {

    alert(num2Letters(parseInt(userEntry, 10)));

}

