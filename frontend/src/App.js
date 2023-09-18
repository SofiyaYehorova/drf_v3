import {useEffect, useState} from 'react'
import {apiService} from "./api.service";

import React from 'react';
import {Chat} from "./Chat";
import {socketService} from "./socket.service";

const App = () => {
    const [cars, setCars] = useState([])

    useEffect(() => {
        apiService.get('/cars').then(value => value.data).then(value => setCars(value.data))
        socketInit()
    }, []);


    const socketInit = async () => {
        const {cars} = await socketService()
        const client = await cars()
        client.onopen = () => {
            console.log('Car socket connected!')
            client.send(JSON.stringify({
                action: 'subscribe_to_cars_activity',
                request_id: new Date().getTime()
            }))
        }
        client.onmessage = (msg) => {
            const data = JSON.parse(msg.data)
            if (data.action==='updata'){
                setCars(prev=>{
                    const car = prev.find(car=>car.id===data.data.id)
                    Object.assign(car, data.data)
                    return [...prev]
                })
            }
        }
    }

    return (
        <div>
            <div>
                {
                    cars.map(car => <div key={car.id}>{car.brand}</div>)
                }
            </div>
            <hr/>
            <div>
                <Chat/>
            </div>
        </div>
    );
};

export {App};
