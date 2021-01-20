using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class MonsterGenerator : MonoBehaviour {
    public GameObject ennemy_prefab;
    public PlayerStats playerStats;
    public CountEnnemyKilled death_counter;
    public VagueController vague_counter;

    private bool isSpawned;
    private int ennemy_number;
    // private float repop_time = 10.0f;

    void Start()
    {
        EnnemyAI EAI = ennemy_prefab.GetComponent<EnnemyAI>();
		EAI.Target = playerStats;
        EAI.count = death_counter;
        EAI.vague = vague_counter;
    }

    void Update(){
        if((!isSpawned)&&(vague_counter.play))
        {
            StartCoroutine("MonsterGeneration");
        }

        if (!(vague_counter.play))
        {
            ennemy_number = 0;
            isSpawned = false;
        }
    }

    IEnumerator MonsterGeneration(){
        if(ennemy_number < 3)
        {
            isSpawned = true;
            Instantiate(ennemy_prefab, transform.position, Quaternion.identity);
            ennemy_number += 1;
            yield return new WaitForSeconds(vague_counter.getRepopTime());
            isSpawned = false;
        }
    }
}