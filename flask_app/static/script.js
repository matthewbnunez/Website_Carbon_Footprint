console.log('hello')
URL = "https://api.websitecarbon.com/site?url="

function getSite(event){
    event.preventDefault()
    siteResultDiv = document.querySelector('#siteResult')
    siteUrl = document.querySelector('#url').value
    console.log(siteUrl)
    siteResultDiv.innerHTML = 'loading...'
    fetch(URL+siteUrl)
        .then(res => res.json())
        .then(data => {
            console.log(data)
            siteResult.innerHTML =`
            <h1>URL: ${data.url}</h1>
            <h1>Green Website hosting: ${data.green}</h1>
            <h1>Cleaner Than ${data.cleanerThan * 100}% of Websites</h1>
            <h1>Co2 from the Grid: ${data.statistics.co2.grid.grams}g</h1>
            <h1>Co2 from the Renewables: ${data.statistics.co2.renewable.grams}g</h1>
            <h1>Energy Consumption: ${data.statistics.energy}KWg</h1>
            `
        })
        .catch(err => console.log(err))
}