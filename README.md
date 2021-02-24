# filtermaker

## Init
```Bash
$> pip install -r equirements.txt
```

## Usage
Take a csv file in argument (WARNING the separator needs to be a `,`)

```Bash
$> python main.py example.csv
```

## Example
```Bash
$> cat exemple.csv
website,instagram
https://playplay.com/
https://filtermaker.fr/

$> python main.py example.csv

$> cat result.csv
websites,instagrams
https://playplay.com/,https://www.instagram.com/tv/B_RZIYPHTGf/ https://www.instagram.com/tv/B4DT5HfIZXI/ https://www.instagram.com/bertrand_usclat/ https://www.instagram.com/deliveroo_fr/ https://www.instagram.com/decathlontalent/ https://www.instagram.com/tv/B6LgKnYK2MJ/ https://www.instagram.com/jiffpom/ https://www.instagram.com/shantybiscuits/ https://www.instagram.com/p/B_FpM42odY9/
https://filtermaker.fr/,https://www.instagram.com/filtermaker.io/

# Bon c'est moche sa mère mais le result.csv passera mieux sur google sheet par exemple (Je n'ai pas fait de petit dessin sur le résultat tu m'en voudras pas)
```
