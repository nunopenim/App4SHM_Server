package com.app4shm.server

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.*

@SpringBootApplication
class ServerApplication
fun main(args: Array<String>) {
    runApplication<ServerApplication>(*args)
}

@RestController
@RequestMapping("/data")
class DataGetter {

    @PostMapping("/reading")
    fun makeData(@RequestBody data: Array<Data>){
        print(data[0].toString() + data[1].toString())
    }
}
