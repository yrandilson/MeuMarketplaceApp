package com.example.meumarketplace.activities
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_filtro.*

class FiltroActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_filtro)
        db = FirebaseFirestore.getInstance()
        btnFiltrar.setOnClickListener {
            val categoria = editTextCategoria.text.toString().trim()
            val precoMax = editTextPrecoMax.text.toString().toDoubleOrNull()
            val query = db.collection("anuncios")
            if (categoria.isNotEmpty()) {
                query.whereEqualTo("categoria", categoria)
            }
            if (precoMax != null) {
                query.whereLessThanOrEqualTo("preco", precoMax)
            }
            query.get().addOnSuccessListener { result ->
                // Retornar resultados para MainActivity
            }
        }
    }
}