package com.example.meumarketplace.activities
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_anuncio.*

class AnuncioActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_anuncio)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        btnPublicar.setOnClickListener {
            val titulo = editTextTitulo.text.toString()
            val descricao = editTextDescricao.text.toString()
            val preco = editTextPreco.text.toString().toDouble()
            val destaque = checkDestaque.isChecked
            val anuncio = hashMapOf(
                "titulo" to titulo,
                "descricao" to descricao,
                "preco" to preco,
                "destaque" to destaque,
                "usuarioId" to auth.currentUser!!.uid,
                "data" to FieldValue.serverTimestamp()
            )
            db.collection("anuncios")
                .add(anuncio)
                .addOnSuccessListener {
                    Toast.makeText(this, "Anúncio publicado!", Toast.LENGTH_SHORT).show()
                    finish()
                }
                .addOnFailureListener {
                    Toast.makeText(this, "Erro ao publicar", Toast.LENGTH_SHORT).show()
                }
        }
    }
}