package com.app4shm.server

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestMethod
import org.springframework.web.bind.annotation.RestController

@SpringBootApplication
class ServerApplication {
    fun main(args: Array<String>) {
        runApplication<ServerApplication>(*args)
    }
}

@RestController
class DataGetter {
    @RequestMapping(value = arrayOf("/data"), method = arrayOf(RequestMethod.POST))
    fun makeData(@RequestBody data: Data) {

    }
}
