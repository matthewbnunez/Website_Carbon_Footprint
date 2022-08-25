console.log('hello')
URL = "https://api.websitecarbon.com/site?url="

function getSite(event){
    event.preventDefault()
    siteResultDiv = document.querySelector('#siteResult')
    siteUrl = document.querySelector('#siteUrl').value
    console.log(siteUrl)
    siteResultDiv.innerHTML = 'loading...'
    fetch(URL+siteUrl)
        .then(res => res.json())
        .then(data => {
            console.log(data)
            siteResult.innerHTML =`
            <h1 class="p-3">URL: ${data.url}</h1>
            <h1 class="p-3">Green Website hosting: ${data.green}</h1>
            <h1 class="p-3">Cleaner Than ${data.cleanerThan * 100}% of Websites</h1>
            <h1 class="p-3">Co2 from the Grid: 0.${Math.floor(data.statistics.co2.grid.grams * 100) / 100}g</h1>
            <h1 class="p-3">Co2 from the Renewables: ${Math.floor(data.statistics.co2.renewable.grams * 100) / 100}g</h1>
            <h1 class="p-3">Energy Consumption: ${data.statistics.energy}KWg</h1>
            `
        })
        .catch(err => console.log(err))
}