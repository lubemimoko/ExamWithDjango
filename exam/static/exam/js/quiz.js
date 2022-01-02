const calTime = ( ()=>{
    let date = new Date()
    let time = date.getHours()*3600 + date.getMinutes()*60 + date.getSeconds()
    let realtime = timevalue - time
    if (realtime < 1){location="/home"}
    // console.log(realtime)
    // alert(realtime)

    let hr = parseInt(realtime/3600) 
    let min = realtime < 3600 ? parseInt(realtime/60) : parseInt((realtime - 3600) / 60)
    let sec =  (realtime ) % 60

    document.getElementById("time").innerText = `${hr}:${min}:${sec}`
})

setInterval(calTime, 1000)


