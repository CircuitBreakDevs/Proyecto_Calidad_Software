import http from 'k6/http';
import { check, sleep } from 'k6';

// Soak Test: Mantiene una carga media durante muchísimo tiempo seguido.
// Su objetivo principal es encontrar fugas de memoria (memory leaks) dado que
// guardamos las partidas en la RAM (diccionarios en el proceso FastAPI).
export const options = {
    stages: [
        { duration: '30s', target: 10 },  // Rampa a 10 VUs
        { duration: '10m', target: 10 },  // Mantener 10 VUs durante 10 minutos (en prod serían horas)
        { duration: '30s', target: 0 },   // Bajar a 0
    ],
};

export default function () {
    const API_URL = __ENV.API_URL || 'http://localhost:8000';

    let payload = JSON.stringify({ nombre_jugador: 'SoakTester' });
    let params = { headers: { 'Content-Type': 'application/json' } };

    // Como cada POST al neuvo juego agranda el diccionario de FastAPI, 
    // esto nos dirá si explota por falta de memoria RAM.
    let res = http.post(`${API_URL}/solo/nuevo`, payload, params);

    check(res, {
        'new game created': (r) => r.status === 200
    });

    sleep(2); // Sleeps más largos para una prueba prolongada pero estable
}
