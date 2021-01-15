using UnityEngine;
// Include the namespace required to use Unity UI
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class MonsterGenerator : MonoBehaviour {
    public GameObject ennemy_prefab;
    public PlayerStats playerStats;

    private bool isSpawned;

    void Start()
    {
        EnnemyAI sn = ennemy_prefab.GetComponent<EnnemyAI>();
		sn.Target = playerStats;
		Instantiate(ennemy_prefab, transform.position, Quaternion.identity);
    }

    void Update(){
        if(!isSpawned)
        {
            StartCoroutine("MonsterGeneration");
        }
    }

    IEnumerator MonsterGeneration(){
        isSpawned = true;
        yield return new WaitForSeconds(5.0f);
        Instantiate(ennemy_prefab, transform.position, Quaternion.identity);
        isSpawned = false;
    }
}