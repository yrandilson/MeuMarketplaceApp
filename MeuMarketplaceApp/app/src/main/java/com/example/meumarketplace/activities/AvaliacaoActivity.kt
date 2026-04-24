package com.example.meumarketplace.activities
import android.os.Bundle
import android.widget.RatingBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FieldValue
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_avaliacao.*

class AvaliacaoActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_avaliacao)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        val anuncioId = intent.getStringExtra("anuncioId") ?: return
        btnAvaliar.setOnClickListener {
            val nota = ratingBar.rating
            val comentario = editTextComentario.text.toString().trim()
            val avaliacao = hashMapOf(
                "nota" to nota,
                "comentario" to comentario,
                "avaliadorId" to auth.currentUser?.uid,
                "data" to FieldValue.serverTimestamp()
            )
            db.collection("anuncios").document(anuncioId)
                .update("avaliacoes", FieldValue.arrayUnion(avaliacao))
                .addOnSuccessListener {
                    Toast.makeText(this, "Avaliação enviada!", Toast.LENGTH_SHORT).show()
                    finish()
                }
                .addOnFailureListener {
                    Toast.makeText(this, "Erro ao avaliar", Toast.LENGTH_SHORT).show()
                }
        }
    }
}