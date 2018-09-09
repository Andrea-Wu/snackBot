var canvas = document.getElemntById('draw');
var ctx = canvas.getContext('2d');

function loop(delay){

    $.ajax({
        contentType: "text/plain; charset=utf-8",
        url: "dump-data",
        type: "GET",
    }).done(function(data){
        data.lines.forEach(function(ln){
            ctx.beginPath();
            ctx.moveTo(ln.x, ln.y);
            ctx.lineTo(ln.x_o, ln.y_o);
            ctx.stroke();
        });
        data.pathq.forEach(function(dest){
            ctx.fillStyle = "red";
            ctx.arc(dest[0], dest[1], 0, 2 * Math.PI);
            ctx.fill();
        });
        ctx.fillStyle = "green";
        ctx.arc(data.arc[0], data.arc[1], 0, 2 * Math.PI);
        ctx.fill();

        setTimeout(function(){
            loop(delay);
        }, delay);
    });
}

loop(500);

function ptLinDist(pt, line){
    m = (line[1] - line[3])/(line[0] - line[2]);
    b = m * line[0] - line[1];
    A = 1/b;
    B = m/b;
    d = Math.abs(pt[0] * A - pt[1] * B)/Math.sqrt(A * A + B * B);
    return d;
}

function insterects(state, mag, line){
    ep_x = state.x + Math.cos(state.deg) * mag
    ep_y = state.y + Math.sin(state.deg) * mag

    m1 = (state.y - ep_y)/(state.x - ep_x);
    m2 = (line[1] - line[3])/(line[0] - line[2]);
    b1 - m1 * state.x - state.y;
    b2 = m2 * line[0] - line[1];

    A1 = 1/b1;
    A2 = 1/b2;
    B1 = m1/b1;
    B2 = m2/b2;
    return A1 * B2 - B1 * A2 != 0 && (mag < 0 || ptLinDist([state.x, state.y], line) < Math.abs(mag));
}

function closestObst(state, mag, obstacles){
    minObst = null; minDist = Math.INFINITY;
    for(obst in obstacles){
        if(intersects(state, data[2], obst) && ptLinDist([state.x, state.y], obst) < minDist){
            minObst = obst;
            minDist =  ptLinDist([state.x, state.y], obst);
        }
    }
    return [minObst, minDist];
}

function sensorData(state, obstacles){
    var closest = closestObst(state, -1, obstacles);
    return [closest[1], closest[1], state.fail];
}

function agent(state, obstacles){

    $.ajax({
        contentType: "text/plain; charset=utf-8",
        url: "robo-update",
        type: "POST",
        data: ",".join(sensorData(state, obstacles))
    }).done(function(data){
        if(data[0] != data[1]){
            setTimeout(function(){
                state.deg += data[2] / (Math.PI * 2);
                state.fail = false;
                agent(state, obstacles);
            }, data[2])
        }else{
            var ob = closestObst(state, data[2], obstacles);
            var minObst = ob[0], minDist = ob[1];
            state.fail = minObst != null;
            var mag = (state.fail)? minDist: data[2];
            state.x = state.x + Math.cos(state.deg) * mag;
            state.y = state.y + Math.sin(state.deg) * mag;
            setTimeout(function(){
                agent(state, obstacles);
            }, data[2]);
        }
    });
}

function makeObstacles(){
    var acc = [];
    for(var i = 0; i < 100; i++){
        acc.push([Math.random()*100, Math.random()*100, Math.random() * 100, Math.random() * 100]);
    }
    return acc;
}
