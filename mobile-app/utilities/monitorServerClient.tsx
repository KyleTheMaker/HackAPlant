import axios from 'axios';
import { useState, useEffect } from 'react';

const API_URL = process.env.EXPO_PULIC_HAP_SERVER_URL as string;

interface PlantMonitorData{
    temperature: number,
    moisture: number,
}


export default function useDeviceData() {
    const [data, setData] = useState<PlantMonitorData | null>(null);

    useEffect(()=>{
    const getData = async () => {
        if(!API_URL){
            console.error("Error Reading data from server!");
            const mockData: PlantMonitorData = {
                temperature: 24.5,
                moisture: 65,
            }
            setData(mockData);
            return;
        }
        try{
            const response = await axios.get(API_URL);
            console.log(response.data);
            const sensorData = response.data;
            setData(sensorData);
        }catch(error){
            console.log(error);
        }
    }
    getData();
    },[]);

return data;

}