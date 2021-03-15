package com.app4shm.server

class Data(val id: String, val timeStamp: Long, val x: Float, val y: Float, val z: Float){
    override fun toString(): String {
        return "ID: ${id} | Timestamp: ${timeStamp} | X: ${x} | Y: ${y} | Z: ${z}\n";
    }
}