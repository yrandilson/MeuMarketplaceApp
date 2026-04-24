package com.example.meumarketplace.activities
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.example.meumarketplace.models.Anuncio
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_detalhe_anuncio.*

class DetalheAnuncioActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detalhe_anuncio)
        db = FirebaseFirestore.getInstance()
        val anuncioId = intent.getStringExtra("anuncioId")
        if (anuncioId != null) {
            db.collection("anuncios").document(anuncioId).get()
                .addOnSuccessListener { document ->
                    val anuncio = document.toObject(Anuncio::class.java)
                    textTitulo.text = anuncio?.titulo
                    textDescricao.text = anuncio?.descricao
                    textPreco.text = "R$ ${anuncio?.preco}"
                }
        }
    }
}