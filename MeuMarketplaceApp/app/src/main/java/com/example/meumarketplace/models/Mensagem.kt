package com.example.meumarketplace.models
data class Mensagem(
    val dePara: String = "",
    val texto: String = "",
    val deUsuarioId: String = "",
    val paraUsuarioId: String = "",
    val data: com.google.firebase.Timestamp? = null
)