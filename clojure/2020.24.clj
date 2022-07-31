(use '[clojure.set :only (intersection, union)])
(use '[io :rename {read-all-lines yummy printI dbg}])
(use '[cartesian :only (move)])
(use '[enum :only (has, make-hash-map)])

; make a graph, follow each path
; pfffft

(defn between [v a b] (and (> v a) (< v b)))

(defn dir [card] 
  (case card
    \e   [1 -1] ; e  -  1, -1
    "se" [1 0]  ; se -  1,  0
    "sw" [0 1]  ; sw -  0,  1
    \w   [-1 1] ; w  - -1,  1
    "nw" [-1 0] ; nw - -1,  0
    "ne" [0 -1] ; ne -  0, -1
    [0 0]
  )
)

(defn neighbors [pos]
  (set (map #(move pos (dir %)) [\e "se" "sw" \w "nw" "ne"]))
  )

(defn parse [line]
; this is where it gets slightly annoying without doing proper parsing
; idiot
    ; if the current token is n or s, also take the next token.
    (loop [[coll [token & more]] [[] line]]
      (if (empty? more)
        (concat coll [token])
        (case token
          \n (recur [(concat coll [(str token (first more))]) (rest more)]) ; wouldn't more rest
          \s (recur [(concat coll [(str token (first more))]) (rest more)]) ; be nice?
          (recur [(concat coll [token]) more])
          )
        )
      )
  )

(defn cancel [coll]
  (loop [acc [] [v & more] coll]
    (if (empty? more)
      (if (has v acc)
        (filter #(not= v %) acc)
        (concat acc [v])
        ) ; this is not elegant but is correct
      (if (has v acc)
        (recur (filter #(not= v %) acc) more)
        (recur (concat acc [v]) more)
        )
    )
  )
) 


(def steps (
  ->> (yummy)
      (map parse)
      (map #(map dir %)) 
      (map #(reduce move [0 0] %))
      (cancel)
  ))

(defn blacked [tile blacks]
  (->> (count (intersection blacks (neighbors tile)))
       (#(if (contains? blacks tile)
           (between % 0 3)
           (= 2 %)
          ))
      )) 

(defn step [blacks]
  (set 
    (filter 
      #(blacked % blacks) 
      (union blacks (apply union (map neighbors blacks)))
      )))

(->> steps
     ((juxt 
       #(->> %
             (count)
             (dbg)
             )
       #(->> %
             (set)
             (iterate step)
             ((fn [coll] (nth coll 100)))
             (count)
             (dbg)
             )

     )))
