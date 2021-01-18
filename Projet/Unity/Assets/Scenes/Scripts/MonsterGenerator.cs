using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class MonsterGenerator : MonoBehaviour {
    public GameObject ennemy_prefab;
    public PlayerStats playerStats;
    public Text death_counter;

    private bool isSpawned;
    private float repop_time = 10.0f;

    void Start()
    {
        EnnemyAI EAI = ennemy_prefab.GetComponent<EnnemyAI>();
		EAI.Target = playerStats;
        EAI.count = death_counter;
    }

    void Update(){
        if(!isSpawned)
        {
            StartCoroutine("MonsterGeneration");
        }
    }

    IEnumerator MonsterGeneration(){
        isSpawned = true;
        Instantiate(ennemy_prefab, transform.position, Quaternion.identity);
        yield return new WaitForSeconds(repop_time);
        isSpawned = false;
    }
}