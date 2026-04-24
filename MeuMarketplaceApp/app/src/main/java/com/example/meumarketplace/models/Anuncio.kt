package com.example.meumarketplace.models
data class Anuncio(
    val id: String = "",
    val titulo: String = "",
    val descricao: String = "",
    val preco: Double = 0.0,
    val destaque: Boolean = false,
    val usuarioId: String = "",
    val data: com.google.firebase.Timestamp? = null,
    val avaliacoes: List<Map<String, Any>> = emptyList()
)