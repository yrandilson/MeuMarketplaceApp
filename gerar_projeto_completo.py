import os

# Estrutura de pastas e arquivos
project_structure = {
    "app/src/main/java/com/example/meumarketplace/activities": [
        "LoginActivity.kt", "CadastroActivity.kt", "MainActivity.kt",
        "AnuncioActivity.kt", "DetalheAnuncioActivity.kt",
        "ChatActivity.kt", "AvaliacaoActivity.kt", "PerfilActivity.kt",
        "FiltroActivity.kt"
    ],
    "app/src/main/java/com/example/meumarketplace/adapters": [
        "AnuncioAdapter.kt", "MensagemAdapter.kt"
    ],
    "app/src/main/java/com/example/meumarketplace/models": [
        "Anuncio.kt", "Usuario.kt", "Mensagem.kt"
    ],
    "app/src/main/res/layout": [
        "activity_login.xml", "activity_cadastro.xml", "activity_main.xml",
        "activity_anuncio.xml", "activity_detalhe_anuncio.xml",
        "activity_chat.xml", "activity_avaliacao.xml", "activity_perfil.xml",
        "activity_filtro.xml", "item_anuncio.xml", "item_mensagem.xml"
    ],
    "app/src/main/res/drawable": [
        "bubble_sent.xml", "bubble_received.xml"
    ],
    "app": ["build.gradle"],
    ".": ["build.gradle", "settings.gradle", "firestore.rules"]
}

# Conteúdo de todos os arquivos
file_contents = {
    # Activities
    "app/src/main/java/com/example/meumarketplace/activities/LoginActivity.kt":
    '''package com.example.meumarketplace.activities
import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import kotlinx.android.synthetic.main.activity_login.*

class LoginActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)
        auth = FirebaseAuth.getInstance()
        btnLogin.setOnClickListener {
            val email = editTextEmail.text.toString()
            val senha = editTextSenha.text.toString()
            auth.signInWithEmailAndPassword(email, senha)
                .addOnCompleteListener(this) { task ->
                    if (task.isSuccessful) {
                        startActivity(Intent(this, MainActivity::class.java))
                    } else {
                        Toast.makeText(this, "Falha no login", Toast.LENGTH_SHORT).show()
                    }
                }
        }
        btnCadastro.setOnClickListener {
            startActivity(Intent(this, CadastroActivity::class.java))
        }
    }
}''',

    "app/src/main/java/com/example/meumarketplace/activities/CadastroActivity.kt":
    '''package com.example.meumarketplace.activities
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_cadastro.*

class CadastroActivity : AppCompatActivity() {
    private lateinit var auth: FirebaseAuth
    private lateinit var db: FirebaseFirestore
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_cadastro)
        auth = FirebaseAuth.getInstance()
        db = FirebaseFirestore.getInstance()
        btnCadastrar.setOnClickListener {
            val email = editTextEmail.text.toString()
            val senha = editTextSenha.text.toString()
            val nome = editTextNome.text.toString()
            val tipo = if (radioPrestador.isChecked) "prestador" else "cliente"
            auth.createUserWithEmailAndPassword(email, senha)
                .addOnCompleteListener(this) { task ->
                    if (task.isSuccessful) {
                        val user = hashMapOf(
                            "nome" to nome,
                            "email" to email,
                            "tipo" to tipo
                        )
                        db.collection("usuarios").document(auth.currentUser!!.uid).set(user)
                            .addOnSuccessListener {
                                Toast.makeText(this, "Cadastro realizado!", Toast.LENGTH_SHORT).show()
                                finish()
                            }
                    } else {
                        Toast.makeText(this, "Erro no cadastro", Toast.LENGTH_SHORT).show()
                    }
                }
        }
    }
}''',

    "app/src/main/java/com/example/meumarketplace/activities/MainActivity.kt":
    '''package com.example.meumarketplace.activities
import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.meumarketplace.adapters.AnuncioAdapter
import com.example.meumarketplace.models.Anuncio
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    private lateinit var anuncioAdapter: AnuncioAdapter
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        anuncioAdapter = AnuncioAdapter(mutableListOf())
        recyclerViewAnuncios.layoutManager = LinearLayoutManager(this)
        recyclerViewAnuncios.adapter = anuncioAdapter
        db.collection("anuncios").get()
            .addOnSuccessListener { result ->
                val anuncios = result.toObjects(Anuncio::class.java)
                anuncioAdapter.updateAnuncios(anuncios)
            }
        btnNovoAnuncio.setOnClickListener {
            startActivity(Intent(this, AnuncioActivity::class.java))
        }
        btnPerfil.setOnClickListener {
            startActivity(Intent(this, PerfilActivity::class.java))
        }
        btnChat.setOnClickListener {
            val intent = Intent(this, ChatActivity::class.java)
            intent.putExtra("outroUsuarioId", "ID_DO_USUARIO_AQUI")
            startActivity(intent)
        }
    }
}''',

    "app/src/main/java/com/example/meumarketplace/activities/AnuncioActivity.kt":
    '''package com.example.meumarketplace.activities
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
}''',

    "app/src/main/java/com/example/meumarketplace/activities/DetalheAnuncioActivity.kt":
    '''package com.example.meumarketplace.activities
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
}''',

    "app/src/main/java/com/example/meumarketplace/activities/ChatActivity.kt":
    '''package com.example.meumarketplace.activities
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.meumarketplace.adapters.MensagemAdapter
import com.example.meumarketplace.models.Mensagem
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.firestore.Query
import kotlinx.android.synthetic.main.activity_chat.*

class ChatActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    private lateinit var mensagemAdapter: MensagemAdapter
    private val mensagens = mutableListOf<Mensagem>()
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_chat)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        val outroUsuarioId = intent.getStringExtra("outroUsuarioId") ?: return
        mensagemAdapter = MensagemAdapter(mensagens)
        recyclerViewMensagens.layoutManager = LinearLayoutManager(this)
        recyclerViewMensagens.adapter = mensagemAdapter
        db.collection("mensagens")
            .whereIn("dePara", listOf(
                "${auth.currentUser?.uid}_$outroUsuarioId",
                "$outroUsuarioId_${auth.currentUser?.uid}"
            ))
            .orderBy("data", Query.Direction.ASCENDING)
            .addSnapshotListener { snapshot, _ ->
                mensagens.clear()
                snapshot?.documents?.forEach { doc ->
                    doc.toObject(Mensagem::class.java)?.let { mensagens.add(it) }
                }
                mensagemAdapter.notifyDataSetChanged()
                recyclerViewMensagens.scrollToPosition(mensagens.size - 1)
            }
        btnEnviar.setOnClickListener {
            val texto = editTextMensagem.text.toString().trim()
            if (texto.isNotEmpty()) {
                val mensagem = Mensagem(
                    dePara = "${auth.currentUser?.uid}_$outroUsuarioId",
                    texto = texto,
                    deUsuarioId = auth.currentUser?.uid ?: "",
                    paraUsuarioId = outroUsuarioId,
                    data = com.google.firebase.Timestamp.now()
                )
                db.collection("mensagens").add(mensagem)
                editTextMensagem.setText("")
            }
        }
    }
}''',

    "app/src/main/java/com/example/meumarketplace/activities/AvaliacaoActivity.kt":
    '''package com.example.meumarketplace.activities
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
}''',

    "app/src/main/java/com/example/meumarketplace/activities/PerfilActivity.kt":
    '''package com.example.meumarketplace.activities
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.android.synthetic.main.activity_perfil.*

class PerfilActivity : AppCompatActivity() {
    private lateinit var db: FirebaseFirestore
    private lateinit var auth: FirebaseAuth
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_perfil)
        db = FirebaseFirestore.getInstance()
        auth = FirebaseAuth.getInstance()
        val usuarioId = auth.currentUser?.uid ?: return
        db.collection("usuarios").document(usuarioId).get()
            .addOnSuccessListener { document ->
                val usuario = document.toObject(com.example.meumarketplace.models.Usuario::class.java)
                textNome.text = usuario?.nome
                textEmail.text = usuario?.email
                textTipo.text = if (usuario?.tipo == "prestador") "Prestador de Serviço" else "Cliente"
            }
    }
}''',

    "app/src/main/java/com/example/meumarketplace/activities/FiltroActivity.kt":
    '''package com.example.meumarketplace.activities
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
}''',

    # Adapters
    "app/src/main/java/com/example/meumarketplace/adapters/AnuncioAdapter.kt":
    '''package com.example.meumarketplace.adapters
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.meumarketplace.R
import com.example.meumarketplace.models.Anuncio

class AnuncioAdapter(private val anuncios: MutableList<Anuncio>) : RecyclerView.Adapter<AnuncioAdapter.AnuncioViewHolder>() {
    class AnuncioViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val textTitulo: TextView = itemView.findViewById(R.id.textTitulo)
        val textPreco: TextView = itemView.findViewById(R.id.textPreco)
    }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): AnuncioViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_anuncio, parent, false)
        return AnuncioViewHolder(view)
    }
    override fun onBindViewHolder(holder: AnuncioViewHolder, position: Int) {
        val anuncio = anuncios[position]
        holder.textTitulo.text = anuncio.titulo
        holder.textPreco.text = "R$ ${anuncio.preco}"
    }
    override fun getItemCount() = anuncios.size
    fun updateAnuncios(novosAnuncios: List<Anuncio>) {
        anuncios.clear()
        anuncios.addAll(novosAnuncios)
        notifyDataSetChanged()
    }
}''',

    "app/src/main/java/com/example/meumarketplace/adapters/MensagemAdapter.kt":
    '''package com.example.meumarketplace.adapters
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import com.example.meumarketplace.R
import com.example.meumarketplace.models.Mensagem
import com.google.firebase.auth.FirebaseAuth

class MensagemAdapter(private val mensagens: List<Mensagem>) : RecyclerView.Adapter<MensagemAdapter.MensagemViewHolder>() {
    class MensagemViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val textMensagem: TextView = itemView.findViewById(R.id.textMensagem)
    }
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MensagemViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_mensagem, parent, false)
        return MensagemViewHolder(view)
    }
    override fun onBindViewHolder(holder: MensagemViewHolder, position: Int) {
        val mensagem = mensagens[position]
        holder.textMensagem.text = mensagem.texto
        if (mensagem.deUsuarioId == FirebaseAuth.getInstance().currentUser?.uid) {
            holder.textMensagem.setBackgroundResource(R.drawable.bubble_sent)
        } else {
            holder.textMensagem.setBackgroundResource(R.drawable.bubble_received)
        }
    }
    override fun getItemCount() = mensagens.size
}''',

    # Models
    "app/src/main/java/com/example/meumarketplace/models/Anuncio.kt":
    '''package com.example.meumarketplace.models
data class Anuncio(
    val id: String = "",
    val titulo: String = "",
    val descricao: String = "",
    val preco: Double = 0.0,
    val destaque: Boolean = false,
    val usuarioId: String = "",
    val data: com.google.firebase.Timestamp? = null,
    val avaliacoes: List<Map<String, Any>> = emptyList()
)''',

    "app/src/main/java/com/example/meumarketplace/models/Usuario.kt":
    '''package com.example.meumarketplace.models
data class Usuario(
    val nome: String = "",
    val email: String = "",
    val tipo: String = ""
)''',

    "app/src/main/java/com/example/meumarketplace/models/Mensagem.kt":
    '''package com.example.meumarketplace.models
data class Mensagem(
    val dePara: String = "",
    val texto: String = "",
    val deUsuarioId: String = "",
    val paraUsuarioId: String = "",
    val data: com.google.firebase.Timestamp? = null
)''',

    # Layouts
    "app/src/main/res/layout/activity_login.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <EditText
        android:id="@+id/editTextEmail"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Email" />
    <EditText
        android:id="@+id/editTextSenha"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Senha"
        android:inputType="textPassword" />
    <Button
        android:id="@+id/btnLogin"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Login" />
    <Button
        android:id="@+id/btnCadastro"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Cadastrar" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_cadastro.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <EditText
        android:id="@+id/editTextNome"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Nome" />
    <EditText
        android:id="@+id/editTextEmail"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Email" />
    <EditText
        android:id="@+id/editTextSenha"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Senha"
        android:inputType="textPassword" />
    <RadioGroup
        android:id="@+id/radioGroupTipo"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">
        <RadioButton
            android:id="@+id/radioPrestador"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Prestador" />
        <RadioButton
            android:id="@+id/radioCliente"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Cliente" />
    </RadioGroup>
    <Button
        android:id="@+id/btnCadastrar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Cadastrar" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_main.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">
        <Button
            android:id="@+id/btnNovoAnuncio"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Novo Anúncio" />
        <Button
            android:id="@+id/btnPerfil"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Perfil" />
        <Button
            android:id="@+id/btnChat"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:text="Chat" />
    </LinearLayout>
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/recyclerViewAnuncios"
        android:layout_width="match_parent"
        android:layout_height="match_parent" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_anuncio.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <EditText
        android:id="@+id/editTextTitulo"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Título" />
    <EditText
        android:id="@+id/editTextDescricao"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Descrição" />
    <EditText
        android:id="@+id/editTextPreco"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Preço"
        android:inputType="numberDecimal" />
    <CheckBox
        android:id="@+id/checkDestaque"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Destaque (Pago)" />
    <Button
        android:id="@+id/btnPublicar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Publicar" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_detalhe_anuncio.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView
        android:id="@+id/textTitulo"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="18sp" />
    <TextView
        android:id="@+id/textDescricao"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />
    <TextView
        android:id="@+id/textPreco"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_chat.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="8dp">
    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/recyclerViewMensagens"
        android:layout_width="match_parent"
        android:layout_height="0dp"
        android:layout_weight="1" />
    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="horizontal">
        <EditText
            android:id="@+id/editTextMensagem"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_weight="1"
            android:hint="Digite uma mensagem" />
        <Button
            android:id="@+id/btnEnviar"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:text="Enviar" />
    </LinearLayout>
</LinearLayout>''',

    "app/src/main/res/layout/activity_avaliacao.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Avalie o serviço:"
        android:textSize="18sp" />
    <RatingBar
        android:id="@+id/ratingBar"
        style="?android:attr/ratingBarStyleSmall"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:numStars="5"
        android:stepSize="1.0" />
    <EditText
        android:id="@+id/editTextComentario"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Comentário (opcional)" />
    <Button
        android:id="@+id/btnAvaliar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Enviar Avaliação" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_perfil.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <TextView
        android:id="@+id/textNome"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:textSize="20sp" />
    <TextView
        android:id="@+id/textEmail"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
    <TextView
        android:id="@+id/textTipo"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content" />
    <Button
        android:id="@+id/btnEditarPerfil"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Editar Perfil" />
</LinearLayout>''',

    "app/src/main/res/layout/activity_filtro.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">
    <EditText
        android:id="@+id/editTextCategoria"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Categoria" />
    <EditText
        android:id="@+id/editTextPrecoMax"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:hint="Preço Máximo"
        android:inputType="numberDecimal" />
    <Button
        android:id="@+id/btnFiltrar"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Filtrar" />
</LinearLayout>''',

    "app/src/main/res/layout/item_anuncio.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="8dp">
    <TextView
        android:id="@+id/textTitulo"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:textSize="16sp" />
    <TextView
        android:id="@+id/textPreco"
        android:layout_width="match_parent"
        android:layout_height="wrap_content" />
</LinearLayout>''',

    "app/src/main/res/layout/item_mensagem.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="4dp">
    <TextView
        android:id="@+id/textMensagem"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:padding="8dp"
        android:textColor="#000000"
        android:textSize="16sp" />
</LinearLayout>''',

    # Drawables
    "app/src/main/res/drawable/bubble_sent.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#DCF8C6" />
    <corners android:radius="8dp" />
    <padding android:left="10dp" android:right="10dp" android:top="5dp" android:bottom="5dp" />
</shape>''',

    "app/src/main/res/drawable/bubble_received.xml":
    '''<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android">
    <solid android:color="#FFFFFF" />
    <stroke android:width="1dp" android:color="#DDDDDD" />
    <corners android:radius="8dp" />
    <padding android:left="10dp" android:right="10dp" android:top="5dp" android:bottom="5dp" />
</shape>''',

    # Gradle e Firestore Rules
    "app/build.gradle":
    '''plugins {
        id 'com.android.application'
        id 'org.jetbrains.kotlin.android'
        id 'com.google.gms.google-services'
    }
    android {
        namespace 'com.example.meumarketplace'
        compileSdk 33
        defaultConfig {
            applicationId "com.example.meumarketplace"
            minSdk 21
            targetSdk 33
            versionCode 1
            versionName "1.0"
            testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        }
        buildTypes {
            release {
                minifyEnabled false
                proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            }
        }
        compileOptions {
            sourceCompatibility JavaVersion.VERSION_1_8
            targetCompatibility JavaVersion.VERSION_1_8
        }
        kotlinOptions {
            jvmTarget = '1.8'
        }
    }
    dependencies {
        implementation 'androidx.core:core-ktx:1.10.1'
        implementation 'androidx.appcompat:appcompat:1.6.1'
        implementation 'com.google.android.material:material:1.9.0'
        implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
        implementation 'com.google.firebase:firebase-auth-ktx:22.1.2'
        implementation 'com.google.firebase:firebase-firestore-ktx:24.9.1'
        implementation 'androidx.recyclerview:recyclerview:1.3.1'
    }''',

    "build.gradle":
    '''// Top-level build file
buildscript {
    ext.kotlin_version = '1.8.0'
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath 'com.android.tools.build:gradle:8.1.0'
        classpath "org.jetbrains.kotlin:kotlin-gradle-plugin:$kotlin_version"
        classpath 'com.google.gms:google-services:4.3.15'
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
task clean(type: Delete) {
    delete rootProject.buildDir
}''',

    "settings.gradle":
    '''rootProject.name = "MeuMarketplaceApp"
include ':app''',

    "firestore.rules":
    '''rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /anuncios/{anuncioId} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth.uid == resource.data.usuarioId;
    }
    match /usuarios/{usuarioId} {
      allow read: if request.auth != null && (request.auth.uid == usuarioId || request.auth.uid == resource.data.usuarioId);
      allow create, update: if request.auth.uid == usuarioId;
      allow delete: if false;
    }
    match /mensagens/{mensagemId} {
      allow read: if request.auth != null &&
        (request.auth.uid == resource.data.deUsuarioId ||
         request.auth.uid == resource.data.paraUsuarioId);
      allow create: if request.auth != null;
      allow update, delete: if false;
    }
  }
}'''
}

def create_project(base_path="MeuMarketplaceApp"):
    for dir_path, files in project_structure.items():
        full_dir_path = os.path.join(base_path, dir_path)
        os.makedirs(full_dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(full_dir_path, file)
            content = file_contents.get(f"{dir_path}/{file}", "")
            if content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                open(file_path, 'w').close()

    for file, content in file_contents.items():
        if "/" not in file:
            file_path = os.path.join(base_path, file)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

if __name__ == "__main__":
    create_project()
    print("Projeto gerado com sucesso na pasta 'MeuMarketplaceApp'!")