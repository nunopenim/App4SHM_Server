package org.app4shm.demo

class Data(val id: String, val timeStamp: Long, val x: Float, val y: Float, val z: Float, val group: String){
    override fun toString(): String {
        return "ID: ${id} | group: ${group} | Timestamp: ${timeStamp} | X: ${x} | Y: ${y} | Z: ${z}\n"
    }

    fun JSONer(): String {
        return "{\"id\": \"${id}\", \"timeStamp\": ${timeStamp}, \"x\": ${x}, \"y\": ${y}, \"z\": ${z}, \"group\": \"${group}\"}"
    }
}