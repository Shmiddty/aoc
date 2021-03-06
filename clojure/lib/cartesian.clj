(ns cartesian)

(use '[enum :only (enumerate, zip, make-hash-map)])

(defn enum2d [mat] (apply conj [] (mapcat
    (fn [[y row]] (map (fn [[x c]] [[x y] c]) (enumerate row)))
    (enumerate mat)
    )))

(defn flatgrid [lines] (apply conj [] (mapcat
    (fn [[y row]] (map (fn [[x c]] [[x y] c]) (enumerate row)))
    (enumerate lines)
    )))

(defn grid [lines]
  (->> lines
       (flatgrid)
       (make-hash-map)
       ))

; is it a bad idea to make this "eager"?
; Well it's prevented a stack-overflow in at least one problem so..?
(defn addvec [a b] (mapv (partial reduce +) (zip a b)))

(defn turn
  ([[x y]] [(- y) x]) ; 90 degrees clockwise (right)
  ([[x y] degrees]
   (if (> 0 degrees)
     (turn [x y] (+ 360 degrees))
     (nth (iterate turn [x y]) (/ degrees 90))
     ))
  )

; mirror along xy
(defn mirror
  ([[x y]] [x (- y)])
  )

(defn move
  ([pos dir] (addvec pos dir))
  ([pos dir n] (nth (iterate (partial addvec dir) pos) n))
  )

(def dirs [
   [-1 -1] [0 -1] [1 -1]
   [-1  0]        [1  0]
   [-1  1] [0  1] [1  1]
   ])

(def neighbors (memoize (fn [pt] (map (partial addvec pt) dirs))))

(def fastneighbors (memoize (fn [[x y]] [
   [(- x 1) (- y 1)] [(+ x 0) (- y 1)] [(+ x 1) (- y 1)]
   [(- x 1) (+ y 0)]                   [(+ x 1) (+ y 0)]
   [(- x 1) (+ y 1)] [(+ x 0) (+ y 1)] [(+ x 1) (+ y 1)]
   ])))

; all adjacent points for all dimensions
; this includes diagonals and the original point
(def zone
  (memoize
    (fn [[d & ds]]
      (if (empty? ds)
        [[(- d 1)] [d] [(+ d 1)]]
        (mapcat
          (fn [DS] (map #(concat % DS) (zone [d])))
          (zone ds)
          )
        ))))

; https://stackoverflow.com/a/21756221
(defn abs [n] (max n (- n)))

(defn manhattan [a b] (reduce + (map abs (addvec a (map #(* -1 %) b)))))
